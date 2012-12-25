from django.conf.urls import patterns, include, url
from django.conf import settings
from dashboard.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forjme.views.home', name='home'),
    # url(r'^forjme/', include('forjme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'dashboard.views.home', name='home'), #HomeView.as_view()
    url(r'^projects/', 'dashboard.views.projects', name='projects'),
    url(r'^project/new', project_new, name="project_new"),
    url(r'^project/info/(?P<project_id>\d+)/$', project_info, name="project_info"),
    url(r'^project/(?P<project_id>\d+)/$', project_edit, name="project_edit"),
    url(r'^accounts/login' , 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}),

    #for django-git
    #(r'^git/', include('django_git.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))