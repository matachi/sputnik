from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from podcasts.views import Podcasts, Podcast, Episode, Feed


urlpatterns = patterns('',
    url(r'^podcasts/$', Podcasts.as_view(), name='podcasts'),
    url(r'^podcasts/(?P<podcast>\d+)$', Podcast.as_view(), name='podcast'),
    url(r'^podcasts/(?P<podcast>\d+)/(?P<episode>\d+)/$', Episode.as_view(), name='episode'),
    url(r'^feed/$', login_required(Feed.as_view()), name='feed'),
)