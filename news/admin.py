from django.contrib import admin
from news.models import NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    filter_horizontal = ('referenced_podcasts', 'referenced_episodes')

admin.site.register(NewsItem, NewsItemAdmin)
