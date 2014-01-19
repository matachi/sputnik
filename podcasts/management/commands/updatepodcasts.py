from django.core.management import BaseCommand
import feedparser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import podcasts
from podcasts.models import Podcast, Tag, Category


class Command(BaseCommand):
    help = 'Initialize podcasts with data from their RSS feeds'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():
            feed_xml = urlopen(podcast.metadata_feed or podcast.feed).read()

            feed = feedparser.parse(feed_xml).feed
            podcast.title = podcast.title if podcast.title_lock else feed.title
            podcast.description = feed.subtitle
            podcast.link = feed.link
            podcast.language = self.get_language(feed)
            podcast.save()
            Command.set_tags(podcast, self.get_tags(feed))
            if getattr(feed, 'image', False):
                podcast.download_image(feed.image.href)

            soup = BeautifulSoup(feed_xml)
            self.set_categories(podcast, soup)

    @staticmethod
    def get_language(feed):
        return feed.language[:2]

    @staticmethod
    def get_category(title):
        try:
            category = Category.objects.get(title=title)
        except Category.DoesNotExist:
            category = Category(title=title)
            category.save()
        return category

    @staticmethod
    def set_categories(podcast, soup):
        for each in soup.find_all('itunes:category'):
            category_title = each['text']
            category = Command.get_category(category_title)
            podcast.categories.add(category)
            for each in each.find_all('itunes:category'):
                sub_category_title = each['text']
                sub_category = Command.get_category(sub_category_title)
                if not sub_category.parent_category:
                    sub_category.parent_category = category
                    sub_category.save()
                podcast.categories.add(sub_category)

    @staticmethod
    def get_tags(feed):
        try:
            return [tag.term for tag in feed.tags]
        except AttributeError:
            return None

    @staticmethod
    def set_tags(podcast, tags):
        if not tags:
            return
        for tag in tags:
            try:
                tag_obj = Tag.objects.get(title=tag)
            except podcasts.models.Tag.DoesNotExist:
                tag_obj = Tag(title=tag)
                tag_obj.save()
            podcast.tags.add(tag_obj)
