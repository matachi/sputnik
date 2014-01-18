from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns
from podcasts.views import Podcasts, Podcast, Episode, Feed, Subscribe, Listened, SubscriptionsOpml, ExportSubscriptions, AddPodcast


urlpatterns = patterns('',
    url(r'^podcasts/$', Podcasts.as_view(), name='podcasts'),
    url(r'^podcasts/category/(\d+)/$', Podcasts.as_view(), name='category'),
    url(r'^podcasts/(\d+)/$', Podcast.as_view(), name='podcast'),
    url(r'^episode/(\d+)/$', Episode.as_view(), name='episode'),
    url(r'^podcasts/add-podcast/$', login_required(AddPodcast.as_view()), name='add-podcast'),
    url(r'^podcasts/export-subscriptions/$', login_required(ExportSubscriptions.as_view()), name='export-subscriptions'),
    url(r'^podcasts/subscriptions.opml$', login_required(SubscriptionsOpml.as_view()), name='subscriptions-opml'),
    url(r'^feed/$', login_required(Feed.as_view()), name='feed'),
    url(r'^subscribe/$', Subscribe.as_view()),
    url(r'^listened/$', Listened.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)