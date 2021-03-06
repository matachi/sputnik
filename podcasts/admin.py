from django.contrib import admin
from django.contrib.messages import constants
import socket

from podcasts.models import Podcast, Episode, PodcastUserProfile, Tag, Category


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1


def update_podcast(modeladmin, request, queryset):
    for podcast in queryset:
        for error in podcast.update():
            if isinstance(error, socket.timeout):
                message = "Downloading {}'s cover image timed out".format(
                    podcast)
                modeladmin.message_user(request, message, constants.WARNING)
update_podcast.short_description = "Update selected podcasts with metadata " +\
                                   "from their feeds"


def fetch_episodes(modeladmin, request, queryset):
    for podcast in queryset:
        podcast.fetch_episodes()
fetch_episodes.short_description = "Fetch new episodes for the selected " +\
                                   "podcasts"


class PodcastAdmin(admin.ModelAdmin):
    inlines = (EpisodeInline,)
    list_display = ('title_or_unnamed', 'feed', 'link')
    actions = [update_podcast, fetch_episodes]

admin.site.register(Podcast, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'published')
    list_filter = ('podcast',)
    search_fields = ('title', 'description')

admin.site.register(Episode, EpisodeAdmin)


class PodcastUserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(PodcastUserProfile, PodcastUserProfileAdmin)


class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
