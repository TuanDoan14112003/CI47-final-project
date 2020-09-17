from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Post,Vote,Comment
from django.dispatch import receiver



@receiver(post_save, sender=Post)
def create_vote(sender, instance, created, **kwargs):
    if created:
        vote = Vote.create(user=instance.author,
                    vote_object=instance,
                    vote_value=1)
        vote.save()


