from django.core.management import BaseCommand
import feedparser
import podcasts
from podcasts.models import Podcast, Tag


class Command(BaseCommand):
    help = 'Initialize podcasts with data from their RSS feeds'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():
            if len(podcast.title):
                # If the podcast already has information
                continue
            feed = feedparser.parse(podcast.feed).feed
            podcast.title = feed.title
            podcast.description = feed.subtitle
            podcast.link = feed.link
            podcast.language = self.get_language(feed)
            podcast.save()
            self.set_tags(podcast, self.get_tags(feed))
            if getattr(feed, 'image', False):
                podcast.download_image(feed.image.href)

    @staticmethod
    def get_language(feed):
        return feed.language[:2]

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
