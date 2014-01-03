from django.contrib import admin
from podcasts.models import Podcast, Episode, PodcastUserProfile


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1


class PodcastAdmin(admin.ModelAdmin):
    inlines = (EpisodeInline,)
    list_display = ('title_or_unnamed', 'feed', 'link')

admin.site.register(Podcast, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')
    list_filter = ('podcast',)
    search_fields = ('title', 'description')

admin.site.register(Episode, EpisodeAdmin)


class PodcastUserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

admin.site.register(PodcastUserProfile, PodcastUserProfileAdmin)
