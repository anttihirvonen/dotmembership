from django.conf.urls import patterns, include, url


urlpatterns = patterns('dotmembership.apps.members.views',
        url(r'^join/$', 'join', name="members-join"),
        url(r'^confirm_join/(?P<token>\w+)$', 'confirm_join', {}, name="members-confirm_join"),
)
