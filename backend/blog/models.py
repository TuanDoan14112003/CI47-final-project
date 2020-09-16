from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from subreddit.models import Subreddit

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.PositiveSmallIntegerField(default=1)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    point = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.content
