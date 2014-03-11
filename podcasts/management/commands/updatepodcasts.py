from django.core.management import BaseCommand
from optparse import make_option
from podcasts.models import Podcast


class Command(BaseCommand):
    help = 'Initialize podcasts with data from their RSS feeds'
    option_list = BaseCommand.option_list + (
        make_option(
            '--only-new',
            action='store_true',
            dest='only_new',
            default=False,
            help='Only update new podcasts'
        ),
    )

    def handle(self, *args, **options):
        for podcast in Podcast.objects.all():
            if options['only_new'] and podcast.title != "":
                continue
            podcast.update()
