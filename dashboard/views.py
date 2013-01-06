# -*- coding: utf-8 -*-

#from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from dashboard.models import Project, Room, News, Event
from dashboard.forms import ProjectForm, ChatForm, NewsForm, EventForm
import django.utils.simplejson as json
from datetime import datetime
from django.http import HttpResponse
from django.template import loader, Context
from django.http import Http404
import logging
from datetime import datetime
#from django.core import serializers

logger = logging.getLogger('dashboard')

@login_required(login_url='/accounts/login/')
def home(request):
	return render_to_response('dashboard/home.html',context_instance=RequestContext(request))

###################################### PROJECTS ################################################
@login_required(login_url='/accounts/login/')
def projects(request):
	projects = Project.objects.all()
	return render_to_response('dashboard/project/projects.html',{'projects':projects}, context_instance=RequestContext(request))	

@login_required(login_url='/accounts/login/')
def project_edit(request, project_id = None):
	try:
		project = Project.objects.get(pk=project_id)
		return render_to_response('dashboard/project/show_project.html',{'project':project}, context_instance=RequestContext(request))        
	except Project.DoesNotExist:
		raise Http404	
	

@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
def chats(request, project_id = None):
	project = Project.objects.get(pk=project_id)
	rooms = Room.objects.filter(project=project)
	return render_to_response('dashboard/chat/chats.html',{'rooms':rooms, 'project':project}, context_instance=RequestContext(request))	

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def show_chat(request, project_id, chat_id):
	project = Project.objects.get(pk=project_id)
	room = Room.objects.get(pk=chat_id)
	return render_to_response('dashboard/chat/show_chat.html', {'room': room, 'project':project}, context_instance=RequestContext(request)) 

@login_required(login_url='/accounts/login/')
def sync_chat(request, project_id, chat_id):
	if request.method != 'POST':
		raise Http404
	post = request.POST

	if not post.get('id', None):
		raise Http404
	r = Room.objects.get(id=post['id'])
	lmid = r.last_message_id()
	return HttpResponse(jsonify({'last_message_id':lmid}))

@login_required(login_url='/accounts/login/')
def send_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.say(request.user, p['message'])
	return HttpResponse('')

@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def join_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.join(request.user)
	return HttpResponse('')

@login_required(login_url='/accounts/login/')
def leave_chat(request, project_id, chat_id):
	p = request.POST
	r = Room.objects.get(id=int(p['chat_room_id']))
	r.leave(request.user)
	return HttpResponse('')

####################################### END CHAT #######################################

####################################### NEWS ###########################################
@login_required(login_url='/accounts/login/')
def news(request, project_id = None):
	logger.debug('les news')
	project = Project.objects.get(pk=project_id)
	news = News.objects.filter(project=project).order_by('-date')
	return render_to_response('dashboard/news/news.html',{'news':news, 'project':project}, context_instance=RequestContext(request))	

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def news_view(request, project_id=None, news_id=None):
	project = Project.objects.get(pk=project_id)
	news = News.objects.get(pk=news_id)
	return render_to_response('dashboard/news/show_news.html',{'news':news, 'project':project}, context_instance=RequestContext(request))	

@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
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