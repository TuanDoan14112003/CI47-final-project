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
)
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('vote/',vote,name = 'vote'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new_comment/', post_comment, name='comment-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

]
