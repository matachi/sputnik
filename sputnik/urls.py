from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('podcasts.urls', 'podcasts')),
    url(r'^', include('news.urls', 'news')),
    url(r'^', include('users.urls', 'users')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
