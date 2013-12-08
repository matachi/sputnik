from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('podcasts.urls', 'podcasts')),
    url(r'^admin/', include(admin.site.urls)),
)
