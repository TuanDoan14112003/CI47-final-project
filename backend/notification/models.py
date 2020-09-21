from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class CustomNotification(models.Model):
    type = models.CharField(default='comment', max_length=30)

    recipient = models.ForeignKey(
        User,
        blank=False,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True)

    actor = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE
    )

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)