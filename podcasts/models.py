from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import io
import lxml
from lxml.html.clean import Cleaner
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import re
from misc.languages import get_language
from podcasts.feed_tools import get_podcast_data


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
    metadata_feed = models.URLField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='podcasts', blank=True)
    language = models.CharField(max_length=2, blank=True)
    tags = models.ManyToManyField(Tag, related_name='podcasts', blank=True)
    categories = models.ManyToManyField(Category, related_name='podcasts',
                                        blank=True)
    title_lock = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:podcast', args=[self.slug or self.id])

    def get_language(self):
        return get_language(self.language) or 'Not specified'

    def image_or_not_found(self):
        return self.image.url if self.image else '{}podcasts/not-found.jpg'.format(settings.MEDIA_URL)

    def title_or_unnamed(self):
        return self.title if self.title else 'unnamed'

    def update_slug(self):
        slug = slugify(self.title)
        # There may already, for some reason, be podcasts in the database
        # with the slug, for example "podcast", "podcast-1" and "podcast-2".
        # So if we want to add yet another podcast with the slug "podcast",
        # we would like to append "-3" to it.
        starting_with_same_slug = Podcast.objects.filter(
            slug__startswith=slug).order_by('slug')
        if len(starting_with_same_slug):
            # Either nothing or a dash with one or more following digits
            pattern = re.compile('^$|^-\d+$')
            # Count the number of podcasts with slugs mentioned above
            have_same_base_slug = len([x for x in starting_with_same_slug if
                                       pattern.match(x.slug[len(slug):])])
            # Add the incremented version number
            slug = '{}-{}'.format(slug, have_same_base_slug + 1)
        self.slug = slug

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

    def update(self, podcast_data=None):
        if not podcast_data:
            # If the method is called without a `podcast_data`
            podcast_data = get_podcast_data(self.metadata_feed or self.feed)
            if not podcast_data:
                # If it wasn't possible to get data, i.e. the page is down
                return
        self.title = self.title if self.title_lock else podcast_data['title']
        self.description = podcast_data['description']
        self.link = podcast_data['link']
        self.language = podcast_data['language']
        if not self.slug:
            self.update_slug()
        self.save()
        self.__set_tags(podcast_data['tags'])
        if podcast_data['image']:
            self.download_image(podcast_data['image'])
        self.__set_categories(podcast_data['categories'])

    @staticmethod
    def __get_category(title):
        try:
            category = Category.objects.get(title=title)
        except Category.DoesNotExist:
            category = Category(title=title)
            category.save()
        return category

    def __set_categories(self, categories):
        for category_key in categories.keys():
            category = self.__get_category(category_key)
            self.categories.add(category)
            for sub_category in categories[category_key]:
                sub_category = self.__get_category(sub_category)
                if not sub_category.parent_category:
                    # If the category isn't set to sub_category's parent
                    sub_category.parent_category = category
                    sub_category.save()
                self.categories.add(sub_category)

    def __set_tags(self, tags):
        if not tags:
            return
        for tag in tags:
            try:
                tag_obj = Tag.objects.get(title=tag)
            except Tag.DoesNotExist:
                tag_obj = Tag(title=tag)
                tag_obj.save()
            self.tags.add(tag_obj)


def add_slug(**kwargs):
    if kwargs['raw']:
        # If it's loaded from a fixture
        instance = kwargs['instance']
        # Create a slug based on the title
        instance.slug = slugify(instance.title)
pre_save.connect(add_slug, sender=Podcast)


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
        # Cleaner documentation: http://lxml.de/lxmlhtml.html#cleaning-up-html
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
