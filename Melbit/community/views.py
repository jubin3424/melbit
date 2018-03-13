from django.contrib import auth
from django.http import HttpResponse, request, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView

from community.forms import PostForm, CommentForm
from .models import Post, Comment
from django.urls import reverse


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.all().order_by('-pk')
    paginate_by = 5


# class PostDetailView(generic.DetailView):
#     model = Post


def post_write(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('community:post_detail', post.pk)
    ctx = {
        'form': form,
    }
    return render(request, 'community/post_write.html', ctx)


def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        return redirect('community:post_detail', post.pk)
    ctx = {
        'form': form,
    }
    return render(request, 'community/post_write.html', ctx)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect(reverse('community:post_list'))


class PostMixinDetailView(DetailView):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Post


class PostDetailJSONView(PostMixinDetailView, DetailView):
    template_name = 'community/post_detail.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        pk = self.kwargs.get('pk')
        context['comments'] = Post.objects.get(pk=pk).comment_set.all()
        return context


def comment_write(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm(request.POST or None)
    if request.POST and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return render(request, 'community/comment.html',
                      {'comment': comment,
                       })
        # return redirect('community:post_detail', post_pk) ajax로 안쓸경우

    return HttpResponse(status=405)
