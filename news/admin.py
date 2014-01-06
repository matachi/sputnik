from django.contrib import admin
from news.models import NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')

admin.site.register(NewsItem, NewsItemAdmin)
