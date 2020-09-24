from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Subreddit(models.Model):
    name = models.CharField(default='default',max_length=50)
    users = models.ManyToManyField(User,related_name='%(class)s_member_of')
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_creator_of')
    cover = models.ImageField(default='default.jpg', upload_to='subreddit_pics')
    avatar = models.ImageField(default='default.jpg', upload_to='subreddit_pics')