from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PersonalUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='personal_profile')
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=20, blank=True)
    facebook = models.CharField(max_length=20, blank=True)
    github = models.CharField(max_length=20, blank=True)
    bitbucket = models.CharField(max_length=20, blank=True)
    visible_email = models.BooleanField(default=False)

    class Meta():
        verbose_name = 'User\'s personal profile'

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('users:settings')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=get_user_model())
def init_podcast_user_profile(instance, created, **kwarg):
    personal_user_profile = PersonalUserProfile(user=instance)
    if created:
        personal_user_profile.save()

