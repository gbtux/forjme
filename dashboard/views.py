# -*- coding: utf-8 -*-

#from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from dashboard.models import Project, Room
from dashboard.forms import ProjectForm, ChatForm
import django.utils.simplejson as json
from datetime import datetime
from django.http import HttpResponse
from django.template import loader, Context
from django.http import Http404

@login_required(login_url='/accounts/login/')
def home(request):
	return render_to_response('dashboard/home.html',context_instance=RequestContext(request))

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
	#return HttpResponse(content=json.dumps({'last_message_id':lmid}), mimetype='application/json')

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