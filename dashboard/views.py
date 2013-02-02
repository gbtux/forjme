# -*- coding: utf-8 -*-

#from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from dashboard.models import Project, Room, News, Event, Page
from dashboard.forms import ProjectForm, ChatForm, NewsForm, EventForm
import django.utils.simplejson as json
from datetime import datetime
from django.http import HttpResponse
from django.template import loader, Context
from django.http import Http404
import logging
from datetime import datetime
from collections import defaultdict
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from dashboard.git.git_client import GitClient 
import os

logger = logging.getLogger('dashboard')

@login_required() #login_url='/accounts/login/'
def home(request):
	return render_to_response('dashboard/home.html',context_instance=RequestContext(request))

###################################### PROJECTS ################################################
@login_required()
def projects(request):
	projects = Project.objects.all()
	return render_to_response('dashboard/project/projects.html',{'projects':projects}, context_instance=RequestContext(request))	

@login_required()
def project_edit(request, project_id = None):
	try:
		project = Project.objects.get(pk=project_id)
		return render_to_response('dashboard/project/show_project.html',{'project':project}, context_instance=RequestContext(request))        
	except Project.DoesNotExist:
		raise Http404	
	

@login_required()
def project_new(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			project = Project.objects.create(name=name, description=description, is_archived = False, creation_date=datetime.now(), creator=request.user)
			project.save()
			tmpl = loader.get_template('dashboard/project/project.html')
			ctx = Context({ 'project': project })
			rendered = tmpl.render(ctx)
			return HttpResponse(content=json.dumps({'success' : 'success', 'element': rendered}), mimetype='application/json')
		else:
			errors = json.dumps(form.errors)
			return HttpResponse(errors, mimetype='application/json')
	else:
		form = ProjectForm(request)
	#variables = RequestContext(request, {'form':form})
	return render_to_response('dashboard/project/newproject.html', {'form':form}, context_instance=RequestContext(request))

#################################### CHAT ###################################################
@login_required()
def chats(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	rooms = Room.objects.filter(project=project)
	return render_to_response('dashboard/chat/chats.html',{'rooms':rooms, 'project':project}, context_instance=RequestContext(request))	

@login_required()
def chat_new(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	if request.method == 'POST':
		form = ChatForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			room = Room.objects.create(title=title, creator=request.user, project=project) 
			room.save()
			tmpl = loader.get_template('dashboard/chat/chat.html')
			ctx = Context({'room':room, 'project': project})
			rendered = tmpl.render(ctx)
			return HttpResponse(content=json.dumps({'success' : 'success', 'element': rendered}), mimetype='application/json')
		else:
			errors = json.dumps(form.errors)
			return HttpResponse(errors, mimetype='application/json')
	else:
		form = ChatForm(request)

	return render_to_response('dashboard/chat/newchat.html', {'form': form, 'project': project}, context_instance=RequestContext(request))

@login_required()
def show_chat(request, project_id, chat_id):
	project = Project.objects.get(pk=project_id)
	room = Room.objects.get(pk=chat_id)
	return render_to_response('dashboard/chat/show_chat.html', {'room': room, 'project':project}, context_instance=RequestContext(request)) 

@login_required()
def sync_chat(request, project_id, chat_id):
	if request.method != 'POST':
		raise Http404
	post = request.POST

	if not post.get('id', None):
		raise Http404
	r = Room.objects.get(id=post['id'])
	lmid = r.last_message_id()
	return HttpResponse(jsonify({'last_message_id':lmid}))

@login_required()
def send_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.say(request.user, p['message'])
	return HttpResponse('')

@login_required()
def receive_chat(request, project_id, chat_id):
	if request.method != 'POST':
		raise Http404
	post = request.POST

	if not post.get('id', None) or not post.get('offset', None):
		raise Http404

	try:
		offset = int(post['offset'])
	except:
		offset = 0

	r = Room.objects.get(id=chat_id)
	m = r.messages(offset)
	return HttpResponse(jsonify(m, ['id','author','message','type']))


@login_required()
def join_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.join(request.user)
	return HttpResponse('')

@login_required()
def leave_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.leave(request.user)
	return HttpResponse('')

####################################### END CHAT #######################################

####################################### NEWS ###########################################
@login_required()
def news(request, project_id = None):
	logger.debug('les news')
	project = Project.objects.get(pk=project_id)
	news = News.objects.filter(project=project).order_by('-date')
	return render_to_response('dashboard/news/news.html',{'news':news, 'project':project}, context_instance=RequestContext(request))	

@login_required()
def news_new(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	#logger.debug('ceci est un test !!!')
	if request.method == 'POST':
		form = NewsForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			news = News.objects.create(title=title, content=content, author=request.user, project=project)
			news.save()
			tmpl = loader.get_template('dashboard/news/new.html')
			ctx = Context({'new':news, 'project': project})
			rendered = tmpl.render(ctx)
			return HttpResponse(content=json.dumps({'success' : 'success', 'element': rendered}), mimetype='application/json')
		else:
			errors = json.dumps(form.errors)
			return HttpResponse(errors, mimetype='application/json')
	else:
		form = NewsForm(request)
	return render_to_response('dashboard/news/newnews.html', {'form': form, 'project': project}, context_instance=RequestContext(request))

@login_required()
def news_view(request, project_id=None, news_id=None):
	project = Project.objects.get(pk=project_id)
	news = News.objects.get(pk=news_id)
	return render_to_response('dashboard/news/show_news.html',{'news':news, 'project':project}, context_instance=RequestContext(request))	

@login_required()
def news_edit(request, project_id=None, news_id=None):
	logger.debug('FIXME : news edit')
	#project = Project.objects.get(pk=project_id)
	#if news_id is None:
	#	news = News()
	#else:
	#	news = News.objects.get(pk=news_id)
	#
	#if request.POST:
	#	raise Http404
	#else:
	#	#form = NewsEditForm(instance=news)
	#	raise Http404
	#variables = RequestContext(request, {'form':form})
	#return render_to_response("dashboard/news/new_news.html", variables)
	raise Http404


############################################## CALENDAR ########################################
@login_required()
def calendar(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	return render_to_response('dashboard/calendar/calendar.html',{'project':project}, context_instance=RequestContext(request))	

def calendar_events(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	events = Event.objects.filter(project=project)
	return HttpResponse(jsonify(events, ['id','title','date_start','date_end','color','all_day']))


def calendar_newevent(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			date_start = form.cleaned_data['date_start']
			logger.debug('date start :  %s' % date_start)
			date_end = form.cleaned_data['date_end']
			if date_start != '':
				dateStart = datetime.strptime(date_start, "%d/%m/%Y %H:%M:%S") #04/01/2013 11:11:45
			else:
				dateStart = None
			if date_end != '':
				dateEnd = datetime.strptime(date_end, "%d/%m/%Y %H:%M:%S")
			else:
				dateEnd = None
			color = form.cleaned_data['color']
			logger.debug('all day %s' % form.cleaned_data['all_day'])
			allday = True if form.cleaned_data['all_day'] == 'true' else False
			#allday = form.cleaned_data['all_day']
			event = Event.objects.create(title=title, date_start=dateStart, date_end=dateEnd, color=color, all_day=allday, project=project)
			event.save()
			return HttpResponse(content=json.dumps({'success' : 'success', 'element': jsonifyO(event, ['id','title','date_start','date_end','color','all_day'])}), mimetype='application/json')
		else:
			errors = json.dumps(form.errors)
			return HttpResponse(errors, mimetype='application/json')
	else:
		form = EventForm(request)
	return render_to_response('dashboard/calendar/newevent.html', {'form': form, 'project': project}, context_instance=RequestContext(request))


############################################## WIKI ########################################
@login_required()
def wiki(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	return render_to_response('dashboard/wiki/wiki.html',{'project':project}, context_instance=RequestContext(request))	

@login_required()
def wiki_list(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	pages = Page.objects.filter(project=project)
	return render_to_response('dashboard/wiki/pages.html',{'pages':pages, 'project':project}, context_instance=RequestContext(request))	

@login_required()
def wiki_page(request, project_id = None, page=None):
	project = Project.objects.get(pk=project_id)
	if request.method == 'GET':
		try:
			page = Page.objects.get(project=project, name=page)
			#page = Page.objects.get(pk=page_id)
			thedate = page.date.strftime("%s %s" % ("%Y-%m-%d", "%H:%M:%S"))
			return HttpResponse(content=json.dumps({'success' : 'success', 'date': thedate, 'creator': page.creator.username, 'content':page.content}), mimetype='application/json')
		except:
			return HttpResponse(content=json.dumps({'success' : 'nopage'}), mimetype='application/json')
	
	if request.method == 'PUT':
		json_data = json.loads(request.raw_post_data)
		if(json_data['isNew']):
			thepage = Page.objects.create(name=page, creator=request.user, project=project)
			thepage.save()
		else:
			thepage = Page.objects.get(project=project, name=page)
			#logger.debug(request.raw_post_data)
			#json_data = json.loads(request.raw_post_data)
        	thepage.content = json_data['content'] 
        	thepage.save()
        return HttpResponse(content=json.dumps({'success' : 'success'}), mimetype='application/json')	


################################# SOURCES ###############################################
@login_required()
def sources(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	branch = repository.get_current_branch()
	repo = 'test.git'
	path = ''
	parent = ''
	branches = repository.get_branches()
	tags = repository.get_tags()
	files = repository.get_tree(branch)
	return render_to_response('dashboard/sources/index.html',{'page':'files', 'files': files.output(), 'repo':repo, 'path': path, 'parent': parent, 'branch': branch, 'branches': branches, 'tags': tags,'project':project}, context_instance=RequestContext(request))	

@login_required()
def sources_forcommit(request, project_id = None, commit=None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	#branch = repository.get_current_branch()
	repo = 'test.git'
	path = ''
	parent = ''
	branches = repository.get_branches()
	tags = repository.get_tags()
	files = repository.get_tree(commit)
	return render_to_response('dashboard/sources/index.html',{'page':'files', 'files': files.output(), 'repo':repo, 'path': path, 'parent': parent, 'branch': commit, 'branches': branches, 'tags': tags,'project':project}, context_instance=RequestContext(request))	


@login_required()
def sources_commits(request, project_id = None, branch = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	repo = 'test.git'
	branches = repository.get_branches()
	tags = repository.get_tags()
	commits = repository.get_commits(branch)
	breadcrumbs = [{'dir': 'Commit history', 'path':''}]
	return render_to_response('dashboard/sources/commits.html',{'page':'commits', 'repo': repo, 'branch': branch, 'branches': branches, 'tags': tags, 'commits': commits, 'project': project, 'breadcrumbs': breadcrumbs}, context_instance=RequestContext(request))	

@login_required()
def sources_commit_history(request, project_id = None, branch = None, file = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	repo = 'test.git'
	branches = repository.get_branches()
	tags = repository.get_tags()
	if file:
		branch = branch + ' -- "' + file + '"' 
	commits = repository.get_commits(branch)
	breadcrumbs = [{'dir': 'Commit history', 'path':''}]
	return render_to_response('dashboard/sources/commits.html',{'page':'commits', 'repo': repo, 'branch': branch, 'branches': branches, 'tags': tags, 'commits': commits, 'project': project, 'breadcrumbs': breadcrumbs}, context_instance=RequestContext(request))	


@login_required()
def sources_commit(request, project_id = None, commit = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	repo = 'test.git'
	thecommit = repository.get_commit(commit)
	breadcrumbs = [{'dir': 'Commit #' + thecommit.hash, 'path':''}]
	return render_to_response('dashboard/sources/commit.html',{'page':'commits', 'repo':repo, 'commit':thecommit, 'project':project, 'breadcrumbs': breadcrumbs},context_instance=RequestContext(request))


@login_required()
def sources_stats(request, project_id = None, branch = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	repo = 'test.git'
	branch = repository.get_current_branch()
	branches = repository.get_branches()
	tags = repository.get_tags()
	stats = repository.get_statistics(branch);
	authors = repository.get_author_statistics()
	breadcrumbs = [{'dir': 'Statistics', 'path':''}]
	return render_to_response('dashboard/sources/stats.html',{'page':'stats', 'repo': repo, 'branch': branch, 'branches': branches, 'tags': tags, 'stats': stats, 'authors': authors, 'project': project, 'breadcrumbs': breadcrumbs}, context_instance=RequestContext(request))	


@login_required()
def sources_file(request, project_id = None, branch = None, file = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	fileType = repository.get_file_type(file)
	blob = repository.get_blob(branch+':"'+file+'"')
	#logger.debug('blob content : %s' % blob.output())
	repo = 'test.git'
	branches = repository.get_branches()
	tags = repository.get_tags()
	output = blob.output()
	breadcrumbs = repository.get_breadcrumbs(file)
	return render_to_response('dashboard/sources/file.html',{'file':file, 'fileType':fileType, 'blob': output, 'repo': repo, 'breadcrumbs':breadcrumbs, 'branch':branch, 'branches':branches,'tags': tags, 'project': project}, context_instance=RequestContext(request))

@login_required()
def sources_tree(request, project_id = None, branch = None, dir = None):
	#logger.debug('directory : %s' % dir)
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	repo = 'test.git'
	branches = repository.get_branches()
	tags = repository.get_tags()
	commits = repository.get_commits(branch)
	path = dir
	if dir.rfind('/') != -1:
		pos = dir.rfind('/')
		parent = dir[0:pos]
	else:
		parent= ''
	files = repository.get_tree(branch+':"'+dir+'"')
	breadcrumbs = repository.get_breadcrumbs(dir)
	return render_to_response('dashboard/sources/index.html',{'page':'files', 'files': files.output(), 'repo':repo, 'path': path, 'parent': parent, 'branch': branch, 'branches': branches, 'tags': tags, 'breadcrumbs': breadcrumbs, 'project':project}, context_instance=RequestContext(request))	


@login_required()
def sources_branch(request, project_id = None, branch = None):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	#branch = repository.get_current_branch()
	repo = 'test.git'
	path = ''
	parent = ''
	branches = repository.get_branches()
	tags = repository.get_tags()
	files = repository.get_tree(branch)
	return render_to_response('dashboard/sources/index.html',{'page':'files', 'files': files.output(), 'repo':repo, 'path': path, 'parent': parent, 'branch': branch, 'branches': branches, 'tags': tags,'project':project}, context_instance=RequestContext(request))	

@login_required()
def sources_archive(request, project_id = None, branch = None, format = 'zip'):
	project = Project.objects.get(pk=project_id)
	client = GitClient()
	repository = client.get_repository('/var/www/git/test.git')
	tree = repository.get_branch_tree(branch)
	archive_dir = settings.FORJME_ARCHIVE_DIR
	file_ouput = repository.create_archive(archive_dir, tree,format)
	response = HttpResponse(FileWrapper(file(file_ouput)), content_type='application/zip')
	response['Content-Length'] = os.path.getsize(file_ouput)
	response['Content-Disposition'] = 'attachment; filename=' + 'test.' + format
	return response


@login_required()
def backlog(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	return render_to_response('dashboard/backlog/backlog.html',{'project':project}, context_instance=RequestContext(request))

################################# UTILS ###############################################

def jsonify(object, fields=None, to_dict=False):
    '''Simple convert model to json'''
    try:
        import json
    except:
        import django.utils.simplejson as json
 
    out = []
    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object
    if to_dict:
        return out
    else:
        return json.dumps(out)


def jsonifyO(object, fields=None):
	tmp = {}
	if fields:
		for field in fields:
			tmp[field] = unicode(object.__getattribute__(field))
	else:
		for attr, value in object.__dict__.iteritems():
			tmp[attr] = value

	return tmp