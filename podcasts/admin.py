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


class PodcastAdmin(admin.ModelAdmin):
    inlines = (EpisodeInline,)
    list_display = ('title_or_unnamed', 'feed', 'link')
    actions = [update_podcast]

admin.site.register(Podcast, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')
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
