from django.conf.urls import url, patterns
from news.views import News

urlpatterns = patterns('',
    url(r'^$', News.as_view(), name='news'),
)
