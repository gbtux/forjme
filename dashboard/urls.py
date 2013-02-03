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

    #sources
    url(r'^project/(?P<project_id>\d+)/sources/archive/(?P<branch>\w+)/(?P<format>\w+)', sources_archive, name="sources_archive"),
    url(r'^project/(?P<project_id>\d+)/sources/tree/(?P<branch>\w+)/(?P<dir>\w.+)', sources_tree, name="sources_tree"),
    url(r'^project/(?P<project_id>\d+)/sources/blob/(?P<branch>\w+)/(?P<file>\w.+)', sources_file, name="sources_file"),
    url(r'^project/(?P<project_id>\d+)/sources/stats/(?P<branch>\w+)', sources_stats, name="sources_stats"),    
    url(r'^project/(?P<project_id>\d+)/sources/commits/(?P<branch>\w+)', sources_commits, name="sources_commits"),
    url(r'^project/(?P<project_id>\d+)/sources/commits/(?P<branch>\w+)/(?P<file>\w.+)', sources_commit_history, name="sources_commit_history"),
    url(r'^project/(?P<project_id>\d+)/sources/commit/(?P<commit>\w+)', sources_commit, name="sources_commit"),
    url(r'^project/(?P<project_id>\d+)/sources/branch/(?P<branch>\w+)', sources_branch, name="sources_branch"),    
    url(r'^project/(?P<project_id>\d+)/sources/(?P<commit>\w+)', sources_forcommit, name="sources_forcommit"),    
    url(r'^project/(?P<project_id>\d+)/sources', sources, name="sources"),    

    #backlog
    url(r'^project/(?P<project_id>\d+)/backlog/usecase/(?P<case_id>\d+)/edit', backlog_usecase_edit, name="backlog_usecase_edit"),
    url(r'^project/(?P<project_id>\d+)/backlog/usecase/new', backlog_new_usecase, name="backlog_new_usecase"),
    url(r'^project/(?P<project_id>\d+)/backlog', backlog, name="backlog"),

    #security
    url(r'^accounts/login' , 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

