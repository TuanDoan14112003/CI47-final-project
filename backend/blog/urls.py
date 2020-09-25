from django.urls import path
from .views import (
    home,
    vote,
    post_comment,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentCreateView,
    ReadAllNotification,
)
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('vote/',vote,name = 'vote'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new_comment/', post_comment, name='comment-create'),
    path('read-all-notification/',ReadAllNotification,name='read-all-notification')
]
