from django.views.generic import ListView
from news.models import NewsItem


class News(ListView):
    model = NewsItem
    template_name = 'news/news.html'
