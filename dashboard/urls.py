from django.conf.urls import patterns, include, url
from django.conf import settings
from dashboard.views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'dashboard.views.home', name='home'), #HomeView.as_view()

    #projects
    url(r'^projects/', projects, name='projects'),
    url(r'^project/new', project_new, name="project_new"),
    url(r'^project/(?P<project_id>\d+)/$', project_edit, name="project_edit"),

    #chat
    url(r'^project/(?P<project_id>\d+)/chats', chats, name="chat_list"),
    url(r'^project/(?P<project_id>\d+)/chat/new', chat_new, name="chat_new"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/sync', sync_chat, name="sync_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/send', send_chat, name="send_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/receive', receive_chat, name="receive_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/join', join_chat, name="join_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)/leave', leave_chat, name="leave_chat"),
    url(r'^project/(?P<project_id>\d+)/chat/(?P<chat_id>\d+)', show_chat, name="show_chat"),

    #news
    url(r'^project/(?P<project_id>\d+)/news/new', news_new, name="news_new"),
    url(r'^project/(?P<project_id>\d+)/news/(?P<news_id>\d+)', news_view, name="news_view"),
    url(r'^project/(?P<project_id>\d+)/news', news, name="news_list"),
    #url(r'^project/(?P<project_id>\d+)/news/edit/(?P<news_id>\d+)', news_edit, name="news_edit"),

    #calendar
    url(r'^project/(?P<project_id>\d+)/calendar/events', calendar_events, name="calendar_events"),
    url(r'^project/(?P<project_id>\d+)/calendar/new', calendar_newevent, name="calendar_newevent"),
    url(r'^project/(?P<project_id>\d+)/calendar', calendar, name="calendar"),

    #wiki
    url(r'^project/(?P<project_id>\d+)/wiki/page/(?P<page>\w+)', wiki_page, name="wiki_page"),
    url(r'^project/(?P<project_id>\d+)/wiki/list', wiki_list, name="wiki_list"),
    url(r'^project/(?P<project_id>\d+)/wiki', wiki, name="wiki"),

    #security
    url(r'^accounts/login' , 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

