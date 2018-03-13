from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'community'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailJSONView.as_view(), name='post_detail'),
    path('<int:post_pk>/comment/write/', views.comment_write, name='comment_write'),
    path('write/', views.post_write, name='post_write'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]