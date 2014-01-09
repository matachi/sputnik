from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from email.utils import formatdate
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from lxml import etree
from podcasts import models
from podcasts.serializers import SubscribeSerializer, ListenedSerializer


class Podcasts(ListView):
    model = models.Podcast
    template_name = 'podcasts/podcasts.html'


class Podcast(ListView):
    template_name = 'podcasts/podcast.html'

    def get_queryset(self):
        self.podcast = get_object_or_404(models.Podcast,
                                         pk=self.kwargs['podcast'])
        return models.Episode.objects.filter(podcast=self.podcast)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcast'] = self.podcast
        if self.request.user.is_authenticated():
            context['subscribed'] = self.podcast in self.request.user.podcasts_profile.subscribed_to.all()
        return context


class Episode(DetailView):
    template_name = 'podcasts/episode.html'

    def get_object(self):
        podcast = get_object_or_404(models.Podcast, pk=self.kwargs['podcast'])
        episode = int(self.kwargs['episode']) - 1
        return models.Episode.objects.filter(podcast=podcast)[episode]


class Feed(ListView):
    template_name = 'podcasts/feed.html'

    def get_queryset(self):
        return models.Episode.objects.filter(
            podcast=self.request.user.podcasts_profile.subscribed_to.all(),
            published__gte='2013-12-01').order_by('-published')


class ExportSubscriptions(TemplateView):
    template_name = 'podcasts/export-subscriptions.html'


class SubscriptionsOpml(View):
    def get(self, request):
        root = etree.Element('opml', attrib={'version': '1.0'})

        head = etree.SubElement(root, 'head')
        title = etree.SubElement(head, 'title')
        title.text = '{}\'s podcast subscriptions'.format(
            self.request.user.username)
        date_created = etree.SubElement(root, 'dateCreated')
        date_created.text = formatdate()

        body = etree.SubElement(root, 'body')
        outline_text = etree.SubElement(body, 'outline',
                                        attrib={'text': 'Podcasts',
                                                'title': 'Podcasts'})
        for podcast in request.user.podcasts_profile.subscribed_to.all():
            etree.SubElement(outline_text, 'outline',
                             attrib={'type': 'rss', 'title': podcast.title,
                                     'text': podcast.title,
                                     'xmlUrl': podcast.feed,
                                     'htmlUrl': podcast.link})
        return HttpResponse(
            etree.tostring(root, encoding='utf-8', xml_declaration=True,
                           pretty_print=True),
            content_type='text/xml')


class Subscribe(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SubscribeSerializer(data=request.DATA)
        if serializer.is_valid():
            podcasts_user_profile = request.user.podcasts_profile
            podcast = models.Podcast.objects.get(pk=serializer.data['podcast'])
            if serializer.data['subscribe']:
                podcasts_user_profile.subscribed_to.add(podcast)
                return Response({'status': 'subscribed'},
                                status=status.HTTP_200_OK)
            else:
                podcasts_user_profile.subscribed_to.remove(podcast)
                return Response({'status': 'unsubscribed'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Listened(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ListenedSerializer(data=request.DATA)
        if serializer.is_valid():
            podcasts_user_profile = request.user.podcasts_profile
            episode = models.Episode.objects.get(pk=serializer.data['episode'])
            if serializer.data['listened']:
                podcasts_user_profile.listened_to.add(episode)
            else:
                podcasts_user_profile.listened_to.remove(episode)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)