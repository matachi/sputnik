import datetime
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
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
from urllib.error import HTTPError

from podcasts import models
from podcasts.feed_tools import get_podcast_data
from podcasts.forms import AddPodcastForm2, AddPodcastForm1
from podcasts.models import Category
from podcasts.serializers import SubscribeSerializer, ListenedSerializer


class Podcasts(ListView):
    template_name = 'podcasts/podcasts.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        # print("IP Address for debug-toolbar: " + self.request.META['REMOTE_ADDR'])
        context = super().get_context_data(**kwargs)
        if len(self.args):
            context['category'] = Category.objects.get(id=self.args[0])
        categories = Category.objects.all()
        context['categories'] = {}
        for category in categories:
            if not category.parent_category:
                if not context['categories'].get(category):
                    context['categories'][category] = []
                continue
            parent = context['categories'].get(category.parent_category)
            if parent:
                parent.append(category)
            else:
                context['categories'][category.parent_category] = [category]
        return context

    def get_queryset(self):
        if len(self.args):
            podcasts = models.Podcast.objects.filter(categories=self.args[0])
        else:
            podcasts = models.Podcast.objects
        return podcasts.exclude(title__exact='')


class Podcast(ListView):
    template_name = 'podcasts/podcast.html'

    def get_queryset(self):
        if len(self.args) > 0:
            self.podcast = get_object_or_404(models.Podcast, pk=self.args[0])
        elif self.kwargs['slug']:
            self.podcast = get_list_or_404(models.Podcast, slug=self.kwargs['slug'])[0]
        return models.Episode.objects.filter(
            podcast=self.podcast).order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcast'] = self.podcast
        context['number_of_subscribers'] = self.podcast.subscribers.count()
        if self.request.user.is_authenticated():
            context['subscribed'] = self.podcast in self.request.user.podcasts_profile.subscribed_to.all()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if len(self.args) > 0 and self.podcast.slug:
            # If the view was called with the podcast's ID and if it has a slug
            return HttpResponseRedirect(self.podcast.get_absolute_url())
        else:
            return response


class AddPodcast(SessionWizardView):
    model = models.Podcast
    template_name = 'podcasts/add-podcast.html'
    form_list = [AddPodcastForm1, AddPodcastForm2]

    def done(self, form_list, **kwargs):
        # Iterator of the wizard's two forms
        forms = iter(form_list)
        # Extract submitted data from the first form
        cleaned_data = next(forms).cleaned_data.copy()
        # Update it with the data from the second form
        cleaned_data.update(next(forms).cleaned_data)

        podcast_data = self.request.session['podcast_data']
        del self.request.session['podcast_data']
        podcast = models.Podcast()
        podcast.feed = cleaned_data['feed']
        if cleaned_data['title'] != podcast_data['title']:
            podcast.title = cleaned_data['title']
            podcast.title_lock = True
            podcast.update_slug()
        podcast.update(podcast_data)
        podcast.save()

        messages.success(self.request,
                         '<strong>Success!</strong> The podcast was ' +
                         'successfully created. Please note that it might ' +
                         'take a few minutes for the episodes to be fetched. ' +
                         '<a href="' + reverse('podcasts:add-podcast') +
                         '" class="alert-link">Add an additional podcast</a>')
        return HttpResponseRedirect(
            reverse('podcasts:podcast', args=(podcast.pk,)))

    def process_step(self, form):
        data = self.get_form_step_data(form).copy()
        if self.steps.current == '0':
            # The form for step 0 has been verified, now check the feed field's
            # URL if it works.
            # If the URL works, try to get some feed data and put it aside
            # inside `data` for the next wizard step. `data` will be returned
            # and stored inside self.storage.
            # `data` is form.data and is of the type QueryDict, here is how to
            # update such a object: https://docs.djangoproject.com/en/dev/ref/request-response/?from=olddocs#django.http.QueryDict.update
            feed_url = data.get('0-feed')
            podcast_data = None
            try:
                podcast_data = get_podcast_data(feed_url)
            except HTTPError:
                form.add_error('feed',
                               'Couldn\'t fetch the page at that  URL, you ' +
                               'probably did a typo.')
            except AttributeError as e:
                if e.args[0] == 'xml':
                    form.add_error('feed', 'Not a valid feed.')
                else:
                    raise e
            if podcast_data:
                self.request.session['podcast_data'] = podcast_data
                new_data = {
                    '0-title': podcast_data['title'],
                    '0-description': podcast_data['description'],
                    '0-link': podcast_data['link']
                }
                if len([x for x in new_data.values() if x == '']) == len(
                        new_data):
                    form.add_error('feed',
                                   'Couldn\'t fetch any feed meta data from ' +
                                   'that URL, are you sure you typed in the ' +
                                   'correct URL to the podcast\'s RSS or ' +
                                   'Atom feed?')
                data.update(new_data)
        return data

    def render_next_step(self, form, **kwargs):
        """
        Need to override render_next_step() and recheck form.is_valid(),
        since process_step() is run after form.is_valid() in the parent's
        post() method, and in the overridden process_step() an error in the
        form could have been risen.
        See source: https://github.com/django/django/blob/1.6.1/django/contrib/formtools/wizard/views.py#L291
        """
        if form.is_valid():
            return super(SessionWizardView, self).render_next_step(form,
                                                                   **kwargs)
        else:
            return self.render(form)

    def get_form_initial(self, step):
        initial_dict = self.initial_dict.get(step, {})
        if step == '1':
            # We use the feed URL from step #0, reads it, and put its data as
            # initial data for the form on step #1, to make it easier for the
            # user.
            # Doc: https://docs.djangoproject.com/en/1.6/ref/contrib/formtools/form-wizard/#django.contrib.formtools.wizard.views.WizardView.get_form_initial
            data = self.storage.get_step_data('0')
            initial_dict.update({
                'title': data.get('0-title'),
                'description': data.get('0-description'),
                'link': data.get('0-link')
            })
        return initial_dict


class Episode(DetailView):
    template_name = 'podcasts/episode.html'

    def get_object(self):
        return models.Episode.objects.get(pk=self.args[0])


class Feed(ListView):
    template_name = 'podcasts/feed.html'

    def get_queryset(self):
        now = timezone.now()
        min_date = now - datetime.timedelta(days=30,
                                            hours=now.hour,
                                            minutes=now.minute,
                                            seconds=now.second,
                                            microseconds=now.microsecond)
        return models.Episode.objects.filter(
            podcast=self.request.user.podcasts_profile.subscribed_to.all(),
            published__gte=min_date).order_by('-published')


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
            podcast = models.Podcast.objects.get(slug=serializer.data['podcast'])
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