from django.conf.urls import url, patterns
from users.views import Profile, Settings, Community

urlpatterns = patterns('',
    url(r'^user/(?P<username>.+)/$', Profile.as_view(), name='profile'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
    url(r'^community/$', Community.as_view(), name='community'),
)
