from django.urls import path
from .views import (
    SubredditCreateView,
    SubredditDetailView
)
from blog.views import PostCreateView
from . import views

urlpatterns = [
    path('new/', SubredditCreateView.as_view(template_name='subreddit/subreddit_form.html'), name='subreddit-create'),
    path('<int:pk>/',SubredditDetailView,name='subreddit-detail'),
    path('<int:pk>/new-post',PostCreateView.as_view(),name='new_subreddit_post'),

]
