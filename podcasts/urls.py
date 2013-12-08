from django.conf.urls import patterns, url
from podcasts.views import PodcastList, EpisodeList


urlpatterns = patterns('',
    url(r'^podcasts/$', PodcastList.as_view(), name='podcasts'),
    url(r'^episodes/$', EpisodeList.as_view(), name='episodes'),
)