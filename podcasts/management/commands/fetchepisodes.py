from django.core.management import BaseCommand
from podcasts.models import Podcast


class Command(BaseCommand):
    help = 'Fetch new podcast episodes'

    def handle(self, *args, **kwargs):
        if len(args):
            podcasts = []
            for arg in args:
                if arg.isdigit():
                    podcasts.extend(Podcast.objects.filter(pk=arg))
                else:
                    podcasts.extend(Podcast.objects.filter(slug=arg))
        else:
            podcasts = Podcast.objects.all()
        for podcast in podcasts:
            podcast.fetch_episodes()
