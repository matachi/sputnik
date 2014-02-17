from django.core.management import BaseCommand
from podcasts.feed_tools import get_podcast_data
from podcasts.models import Podcast, Tag, Category


class Command(BaseCommand):
    help = 'Initialize podcasts with data from their RSS feeds'

    def handle(self, *args, **kwargs):
        for podcast in Podcast.objects.all():

            podcast_data = get_podcast_data(
                podcast.metadata_feed or podcast.feed)

            podcast.title = podcast.title if podcast.title_lock else \
                podcast_data['title']
            podcast.description = podcast_data['subtitle']
            podcast.link = podcast_data['link']
            podcast.language = podcast_data['language']
            podcast.save()

            Command.set_tags(podcast, podcast_data['tags'])
            if podcast_data['image']:
                podcast.download_image(podcast_data['image'])
            Command.set_categories(podcast, podcast_data['categories'])

    @staticmethod
    def get_category(title):
        try:
            category = Category.objects.get(title=title)
        except Category.DoesNotExist:
            category = Category(title=title)
            category.save()
        return category

    @staticmethod
    def set_categories(podcast, categories):
        for category in categories.keys():
            category = Command.get_category(category)
            podcast.categories.add(category)
            for sub_category in categories[category]:
                sub_category = Command.get_category(sub_category)
                if not sub_category.parent_category:
                    # If the category isn't set to sub_category's parent
                    sub_category.parent_category = category
                    sub_category.save()
                podcast.categories.add(sub_category)

    @staticmethod
    def set_tags(podcast, tags):
        if not tags:
            return
        for tag in tags:
            try:
                tag_obj = Tag.objects.get(title=tag)
            except Tag.DoesNotExist:
                tag_obj = Tag(title=tag)
                tag_obj.save()
            podcast.tags.add(tag_obj)
