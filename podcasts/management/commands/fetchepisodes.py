from django.core.management import BaseCommand
import feedparser
from podcasts.models import Podcast, Episode


class Command(BaseCommand):
    help = 'Fetch new podcast episodes'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():
            episodes = podcast.episode_set
            feed = feedparser.parse(podcast.feed)
            for feed_episode in feed.entries:
                if len(episodes.filter(link=feed_episode.link)):
                    # If the episode already is in the DB
                    continue
                episode = Episode(title=feed_episode.title,
                                  link=feed_episode.link,
                                  description=feed_episode.summary,
                                  podcast=podcast)
                episode.save()
