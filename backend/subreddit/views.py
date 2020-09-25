from django.shortcuts import render
from django.views.generic import (
    CreateView,
)
from .models import Subreddit
from blog.models import Post,Comment,Vote
# Create your views here.
class SubredditCreateView(CreateView):
    model = Subreddit
    fields = ['name','description','cover', 'avatar']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

def SubredditDetailView(request,pk):
    subreddit = Subreddit.objects.get(id=pk)
    posts = Post.objects.filter(subreddit=subreddit)
    post_votes = {}
    if request.user.is_authenticated:
        for post in posts:
            try:
                vote = Vote.objects.get(
                    vote_object_type=post.get_content_type(),
                    vote_object_id=post.id,
                    user=request.user)
                post_votes[post.id] = vote.value

            except Vote.DoesNotExist:
                pass
    notifications = request.user.notifications.order_by('-timestamp')
    return render(request, 'subreddit/subreddit_detail.html', {'posts'     : posts,
                                                'subreddit': subreddit,
                                                'post_votes': post_votes,
                                                'notifications': notifications,
                                                'unread_notifications':  len(request.user.notifications.filter(unread=True))}
                                                     )