from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import io
import lxml
from lxml.html.clean import Cleaner
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from misc.languages import get_language


class Tag(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=30)
    parent_category = models.ForeignKey('self', related_name='child_category',
                                        blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:category', args=[self.id])


class Podcast(models.Model):
    title = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    feed = models.URLField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='podcasts')
    language = models.CharField(max_length=2, blank=True)
    tags = models.ManyToManyField(Tag, related_name='podcasts', blank=True)
    categories = models.ManyToManyField(Category, related_name='podcasts',
                                        blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:podcast', args=[self.id])

    def get_language(self):
        return get_language(self.language) or 'Not specified'

    def image_or_not_found(self):
        return self.image.url if self.image else '{}podcasts/not-found.jpg'.format(settings.MEDIA_URL)

    def title_or_unnamed(self):
        return self.title if self.title else 'unnamed'

    def download_image(self, url):
        # How to save an img from the net in a Django model:
        # http://stackoverflow.com/a/2141823/595990

        # Download the image to memory
        image = io.BytesIO(urlopen(url).read())
        # Now resize the image using Pillow
        image = Image.open(image)
        image = image.resize((400, 400), Image.ANTIALIAS)
        # Create a temp file and save Pillow's image to the file
        image_tmp = NamedTemporaryFile(delete=True)
        image.save(image_tmp.name, 'JPEG', quality=75)
        # Add the album art to the podcast
        self.image.save('{}.jpg'.format(self.pk), File(image_tmp))
        # Close and delete the temp image
        image_tmp.close()


class Episode(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    podcast = models.ForeignKey(Podcast, related_name='episodes')
    published = models.DateTimeField(blank=True)
    audio_file = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:episode', args=[self.id])

    def cleaned_description(self):
        if not self.description:
            # If the description is empty, just return an empty string
            return ''
        cleaner = Cleaner(links=False, page_structure=True,
                          remove_tags=['body'])
        try:
            # Try to return a cleaned description
            cleaned = cleaner.clean_html(self.description)
            return cleaned
        except lxml.etree.ParserError as e:
            # Exception will be thrown if the description, for example, is just
            # some whitespaces
            if e.args[0] == 'Document is empty':
                return ''
            else:
                raise e


class PodcastUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='podcasts_profile')
    subscribed_to = models.ManyToManyField(Podcast, related_name='subscribers',
                                           blank=True)
    listened_to = models.ManyToManyField(Episode, related_name='listeners',
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
