from django.apps import AppConfig


class SubredditConfig(AppConfig):
    name = 'subreddit'
    def ready(self):
        import subreddit.signals

