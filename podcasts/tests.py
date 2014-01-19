from unittest import TestCase
from podcasts.models import Episode


class EpisodeTestCase(TestCase):
    def test_cleaned_description(self):
        episode = Episode(title='Test')
        self.assertEqual('', episode.cleaned_description(),
                         'Empty description should return an empty string')
        episode.description = '    '
        self.assertEqual('', episode.cleaned_description(),
                         'White spaces should be cleaned to an empty string')
        episode.description = 'Olivia Dunham'
        self.assertEqual('<p>Olivia Dunham</p>', episode.cleaned_description(),
                         'Non-empty string should return cleaned result')
        episode.description = '<iframe>'
        self.assertEqual('<div></div>', episode.cleaned_description())
