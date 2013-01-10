from django.conf.urls import patterns, include, url
from django.conf import settings
from dashboard.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^', include('dashboard.urls')),
    #url(r'^forjme//', include('forjme.dashboard.urls')),
    
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))