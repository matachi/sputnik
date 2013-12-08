from django.views.generic import ListView
from podcasts.models import Podcast, Episode


class PodcastList(ListView):
    model = Podcast


class EpisodeList(ListView):
    model = Episode
