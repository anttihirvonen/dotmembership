from django.conf.urls import patterns, include, url
from .views import confirm_join


urlpatterns = patterns('',
        url(r'^confirm_join/(?P<token>\w+)$', confirm_join, {}, name="members-confirm_join"),
)
