from django.contrib import admin
from podcasts.models import Podcast, Episode


class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title_or_unnamed', 'feed', 'link')

admin.site.register(Podcast, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')

admin.site.register(Episode, EpisodeAdmin)
