# -*- coding: utf-8 -*-

#from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from dashboard.models import Project
from dashboard.forms import ProjectForm
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
	return render_to_response('dashboard/projects.html',{'projects':projects}, context_instance=RequestContext(request))	

@login_required(login_url='/accounts/login/')
def project_edit(request, project_id = None):
	try:
		project = Project.objects.get(pk=project_id)
		return render_to_response('dashboard/show_project.html',{'project':project}, context_instance=RequestContext(request))        
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
			tmpl = loader.get_template('dashboard/project.html')
			ctx = Context({ 'project': project })
			rendered = tmpl.render(ctx)
			return HttpResponse(content=json.dumps({'success' : 'success', 'element': rendered}), mimetype='application/json')
		else:
			errors = json.dumps(form.errors)
			return HttpResponse(errors, mimetype='application/json')
	else:
		form = ProjectForm(request)
	#variables = RequestContext(request, {'form':form})
	return render_to_response('dashboard/newproject.html', {'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def project_info(request, projectId = None):
	project = get_object_or_404(Task, pk=projectId)
	render_to_response('dashboard/project', {'project': project})
