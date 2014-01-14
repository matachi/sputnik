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
                        # break and don't check any more episodes in this feed
                        break
                except AttributeError:
                    # The episode in the feed doesn't have a title
                    continue
                episode = Episode(
                    podcast=podcast,
                    title=feed_episode.title,
                    link=self.get_link(feed_episode),
                    description=self.get_description(feed_episode),
                    published=self.get_published(feed_episode),
                    audio_file=self.get_audio_file(feed_episode),
                )
                episode.save()

    @staticmethod
    def get_link(episode):
        return getattr(episode, 'link', '')

    @staticmethod
    def get_published(episode):
        # parser.parse(): http://stackoverflow.com/a/18726020/595990
        return parser.parse(episode.published)

    @staticmethod
    def get_audio_file(episode):
        enclosures = getattr(episode, 'enclosures', '')
        for enclosure in enclosures:
            if enclosure.type[:5] == 'audio':
                return enclosures[0].href
        return ''

    @staticmethod
    def get_description(episode):
        summary = getattr(episode, 'summary', None)
        if summary:
            return summary
        content = getattr(episode, 'content', None)
        if content:
            return content[0].value
        return ''
