from django.urls import re_path

from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/like-comment-notification/$', NotificationConsumer),
]