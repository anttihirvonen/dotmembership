from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dotmembership.views.home', name='home'),
    # url(r'^dotmembership/', include('dotmembership.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'dotmembership.apps.members.views.index', name="index"),
    url(r'^admin/', include(admin.site.urls)),
)
