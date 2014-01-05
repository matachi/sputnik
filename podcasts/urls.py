from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns
from podcasts.views import Podcasts, Podcast, Episode, Feed, Subscribe


urlpatterns = patterns('',
    url(r'^podcasts/$', Podcasts.as_view(), name='podcasts'),
    url(r'^podcasts/(?P<podcast>\d+)$', Podcast.as_view(), name='podcast'),
    url(r'^podcasts/(?P<podcast>\d+)/(?P<episode>\d+)/$', Episode.as_view(), name='episode'),
    url(r'^feed/$', login_required(Feed.as_view()), name='feed'),
    url(r'^subscribe/$', Subscribe.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)