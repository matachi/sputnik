from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.utils.dateparse import parse_datetime
from unittest import mock
from podcasts.models import Episode
from podcasts.views import Feed


class EpisodeTestCase(TestCase):
    def test_cleaned_description(self):
        episode = Episode(title='Test')
        self.assertEqual(episode.cleaned_description(), '',
                         'Empty description should return an empty string')
        episode.description = '    '
        self.assertEqual(episode.cleaned_description(), '',
                         'White spaces should be cleaned to an empty string')
        episode.description = 'Olivia Dunham'
        self.assertEqual(episode.cleaned_description(), '<p>Olivia Dunham</p>',
                         'Non-empty string should return cleaned result')
        episode.description = '<iframe>'
        self.assertEqual(episode.cleaned_description(), '<div></div>')


class FeedTestCase(TestCase):
    fixtures = ['test_setup.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.factory = RequestFactory()

    @mock.patch('podcasts.views.timezone')
    def test_get_queryset(self, mock_timezone):
        mock_timezone.now.return_value = parse_datetime(
            '2014-02-01T20:00:00+00:00')

        # https://docs.djangoproject.com/en/dev/topics/testing/advanced/#the-request-factory
        request = self.factory.get(reverse('podcasts:feed'))
        request.user = self.user

        response = Feed.as_view()(request)
        self.assertEqual(len(response.context_data['episode_list'].all()), 2)
