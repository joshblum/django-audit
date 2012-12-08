from django.conf.urls import patterns, include, url
from django.conf import settings
from django.shortcuts import HttpResponse
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^forum/', include('forum.urls')),
    url(r'^todo/', include('todo.urls')),
)

urlpatterns += patterns('django_audit.views',
    url(r'accounts/profile', 'home'),
)