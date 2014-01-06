from django.conf import settings
from django.db import models
from podcasts.models import Episode, Podcast


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    published = models.DateTimeField()
    stickied = models.BooleanField()
    referenced_podcasts = models.ManyToManyField(Podcast,
                                                 related_name='news_items',
                                                 blank=True)
    referenced_episodes = models.ManyToManyField(Episode,
                                                 related_name='news_items',
                                                 blank=True)

    def __str__(self):
        return self.title