from django.core.management import BaseCommand
from podcasts.models import Podcast


class Command(BaseCommand):
    help = 'Initialize podcasts with data from their RSS feeds'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():
            podcast.update()
