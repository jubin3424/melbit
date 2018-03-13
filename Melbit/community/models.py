from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hitcount.models import HitCount


class Post(models.Model):
    user = models.CharField(max_length=15)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    file = models.FileField(blank=True)
    photo = models.ImageField(blank=True, upload_to="board/%Y/%m/%d")
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.content
