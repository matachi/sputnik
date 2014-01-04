from django.conf.urls import patterns, url
from podcasts.views import Podcasts, Podcast, Episode, Feed


urlpatterns = patterns('',
    url(r'^podcasts/$', Podcasts.as_view(), name='podcasts'),
    url(r'^podcasts/(?P<podcast>\d+)$', Podcast.as_view(), name='podcast'),
    url(r'^podcasts/(?P<podcast>\d+)/(?P<episode>\d+)/$', Episode.as_view(), name='episode'),
    url(r'^feed/$', Feed.as_view(), name='feed'),
)