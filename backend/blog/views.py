from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseBadRequest, Http404, \
    HttpResponseForbidden
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from channels.layers import get_channel_layer
from .models import Post, Comment,Vote
from django_project.utils.helpers import post_only

def home(request):
    posts = Post.objects.all()
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
    print(post_votes)

    return render(request, 'blog/home.html', {'posts'     : posts,
                                                     'post_votes': post_votes})

# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

def post_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': "You need to log in to post new comments."})
    parent_type = request.POST.get('parentType', None)
    parent_id = request.POST.get('parentId', None)
    raw_comment = request.POST.get('commentContent', None)

    if not all([parent_id, parent_type]) or \
            parent_type not in ['comment', 'post'] or \
        not parent_id.isdigit():
        return HttpResponseBadRequest()

    if not raw_comment:
        return JsonResponse({'msg': "You have to write something."})
    author = request.user
    parent_object = None
    try:  # try and get comment or submission we're voting on
        if parent_type == 'comment':
            parent_object = Comment.objects.get(id=parent_id)
        elif parent_type == 'post':
            parent_object = Post.objects.get(id=parent_id)

    except (Comment.DoesNotExist, Post.DoesNotExist):
        return HttpResponseBadRequest()

    comment = Comment.create(author=author,
                             raw_comment=raw_comment,
                             parent=parent_object)

    comment.save()
    return JsonResponse({'msg': "Your comment has been posted."})

def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(author=request.user, content=request.POST.get('content'))
        notification = CustomNotification.objects.create(type="comment", recipient=post.author, actor=request.user, verb="commented on your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.author.username)
        print(json.dumps(NotificationSerializer(notification).data))
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))

@post_only
def vote(request):
    # The type of object we're voting on, can be 'submission' or 'comment'
    vote_object_type = request.POST.get('what', None)

    # The ID of that object as it's stored in the database, positive int
    vote_object_id = request.POST.get('what_id', None)

    # The value of the vote we're writing to that object, -1 or 1
    # Passing the same value twice will cancel the vote i.e. set it to 0
    new_vote_value = request.POST.get('vote_value', None)

    # By how much we'll change the score, used to modify score on the fly
    # client side by the javascript instead of waiting for a refresh.
    vote_diff = 0

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        user = request.user

    try:  # If the vote value isn't an integer that's equal to -1 or 1
        # the request is bad and we can not continue.
        new_vote_value = int(new_vote_value)

        if new_vote_value not in [-1, 1]:
            raise ValueError("Wrong value for the vote!")

    except (ValueError, TypeError):
        return HttpResponseBadRequest()

    # if one of the objects is None, 0 or some other bool(value) == False value
    # or if the object type isn't 'comment' or 'submission' it's a bad request
    if not all([vote_object_type, vote_object_id, new_vote_value]) or \
            vote_object_type not in ['comment', 'post']:
        return HttpResponseBadRequest()

    # Try and get the actual object we're voting on.
    try:
        if vote_object_type == "comment":
            vote_object = Comment.objects.get(id=vote_object_id)

        elif vote_object_type == "post":
            vote_object = Post.objects.get(id=vote_object_id)
        else:
            return HttpResponseBadRequest()  # should never happen

    except (Comment.DoesNotExist, Post.DoesNotExist):
        return HttpResponseBadRequest()

    # Try and get the existing vote for this object, if it exists.
    try:
        vote = Vote.objects.get(vote_object_type=vote_object.get_content_type(),
                                vote_object_id=vote_object.id,
                                user=user)

    except Vote.DoesNotExist:
        # Create a new vote and that's it.
        vote = Vote.create(user=user,
                           vote_object=vote_object,
                           vote_value=new_vote_value)
        vote.save()
        vote_diff = new_vote_value
        return JsonResponse({'error'   : None,
                             'voteDiff': vote_diff})

    # User already voted on this item, this means the vote is either
    # being canceled (same value) or changed (different new_vote_value)
    if vote.value == new_vote_value:
        # canceling vote
        vote_diff = vote.cancel_vote()
        if not vote_diff:
            return HttpResponseBadRequest(
                'Something went wrong while canceling the vote')
    else:
        # changing vote
        vote_diff = vote.change_vote(new_vote_value)
        if not vote_diff:
            return HttpResponseBadRequest(
                'Wrong values for old/new vote combination')

    return JsonResponse({'error'   : None,
                         'voteDiff': vote_diff})



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def PostDetailView(request, pk=None):
    """
    Handles comment view when user opens the thread.
    On top of serving all comments in the thread it will
    also return all votes user made in that thread
    so that we can easily update comments in template
    and display via css whether user voted or not.

    :param thread_id: Thread ID as it's stored in database
    :type thread_id: int
    """

    this_post = get_object_or_404(Post, id=pk)

    thread_comments = Comment.objects.filter(post=this_post)

    if request.user.is_authenticated:
        try:
            reddit_user = request.user
        except RedditUser.DoesNotExist:
            reddit_user = None
    else:
        reddit_user = None

    sub_vote_value = None
    comment_votes = {}

    if reddit_user:
        try:
            vote = Vote.objects.get(
                vote_object_type=this_post.get_content_type(),
                vote_object_id=this_post.id,
                user=reddit_user)
            sub_vote_value = vote.value
        except Vote.DoesNotExist:
            pass

        try:
            user_thread_votes = Vote.objects.filter(author=reddit_user,
                                                    post=this_post)

            for vote in user_thread_votes:
                comment_votes[vote.vote_object.id] = vote.value
        except:
            pass

    return render(request, 'blog/post_detail.html',
                  {'object'   : this_post,
                   'comments'     : thread_comments,
                   'comment_votes': comment_votes,
                   'sub_vote'     : sub_vote_value})


# class PostDetailView(DetailView):
#     model = Post

#     def get_context_data(self, **kwargs):
#         post = get_object_or_404(Post, pk=self.kwargs['pk'])
#         context = super().get_context_data(**kwargs)
#         context['comments'] = post.comments.order_by('-timestamp')
#         try:
#             vote = Vote.objects.get(
#                 vote_object_type=post.get_content_type(),
#                 vote_object_id=post.id,
#                 user=self.request.user)
#             context['vote_value'] = vote.value
#         except Vote.DoesNotExist:
#             pass
#         return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)
