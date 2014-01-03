from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Podcast(models.Model):
    title = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    feed = models.URLField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def title_or_unnamed(self):
        return self.title if self.title else 'unnamed'


class Episode(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    podcast = models.ForeignKey(Podcast)
    published = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class PodcastUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed_to = models.ManyToManyField(Podcast, related_name='subscribers',
                                           blank=True)

    class Meta():
        verbose_name = 'User\'s Podcasts profile'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=get_user_model())
def init_podcast_user_profile(instance, created, **kwarg):
    podcast_user_profile = PodcastUserProfile(user=instance)
    if created:
        podcast_user_profile.save()
