from django.conf.urls import url, patterns
from users.views import Profile, Settings

urlpatterns = patterns('',
    url(r'^user/(?P<username>.+)/$', Profile.as_view(), name='profile'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
)
