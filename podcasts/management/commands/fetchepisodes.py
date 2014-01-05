from dateutil import parser
from django.core.management import BaseCommand
import feedparser
from podcasts.models import Podcast, Episode


class Command(BaseCommand):
    help = 'Fetch new podcast episodes'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():
            episodes = podcast.episodes
            feed = feedparser.parse(podcast.feed)
            for feed_episode in feed.entries:
                try:
                    if len(episodes.filter(podcast=podcast).filter(
                            title=feed_episode.title)):
                        # If the episode already is in the DB
                        continue
                except AttributeError:
                    # The episode in the feed doesn't have a title
                    continue
                    # parser.parse(): http://stackoverflow.com/a/18726020/595990
                enclosures = getattr(feed_episode, 'enclosures', '')
                audio_file = ''
                for enclosure in enclosures:
                    if enclosure.type[:5] == 'audio':
                        audio_file = enclosures[0].href
                        break
                episode = Episode(title=feed_episode.title,
                                  link=getattr(feed_episode, 'link', ''),
                                  description=feed_episode.summary,
                                  podcast=podcast,
                                  published=parser.parse(
                                      feed_episode.published),
                                  audio_file=audio_file,
                )
                episode.save()
