from django.conf.urls import patterns, url


urlpatterns = patterns('dotmembership.apps.members.views',
        # Normal views
        url(r'^edit/(?P<signed_id>.+)$', 'edit', name="members-edit_member"),
        url(r'^confirm_join/(?P<token>\w+)$', 'confirm_join', {}, name="members-confirm_join"),
        # AJAX views
        url(r'^join/$', 'join', name="members-join"),
        url(r'^send_edit_link/$', 'send_edit_link', name="members-send_edit_link"),
)
