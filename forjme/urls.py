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

    url(r'^projects/', projects, name='projects'),
    url(r'^project/new', project_new, name="project_new"),
    url(r'^project/(?P<project_id>\d+)/$', project_edit, name="project_edit"),

    url(r'^project/(?P<project_id>\d+)/chats', chats, name="chat_list"),
    url(r'^project/(?P<project_id>\d+)/chat/new', chat_new, name="chat_new"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/sync', sync_chat, name="sync_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/send', send_chat, name="send_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/receive', receive_chat, name="receive_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/join', join_chat, name="join_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/leave', leave_chat, name="leave_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)', show_chat, name="show_chat"),
    
    url(r'^accounts/login' , 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}),

    #for django-git
    #(r'^git/', include('django_git.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))