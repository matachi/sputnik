from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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