from django.core.management import BaseCommand
import feedparser
from podcasts.models import Podcast


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
            podcast.save()
