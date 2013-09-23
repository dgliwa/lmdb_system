from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from reference.models import Event, Project, Parameter, Project, Permit, People

from django.http import *
from django.shortcuts import render_to_response,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from forms import ParamForm, PermitForm, EventForm, ProjectForm

import random #will be removed later, need to update database


@login_required(login_url='/login/')
def index(request):
    
    return render(request,'reference/reference.html',{})


#########################################################################################
#   BEGINNING OF FUNCTIONS FOR EVENTS #
#########################################################################################
    
@login_required(login_url='/login/')
def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    person = get_object_or_404(People, pk=event.personid.objectid)
    projects = Project.objects.get_query_set().filter(eventid=event.objectid)
    return render(request, 'reference/eventDetail.html', {'event' : event, 'person' : person, 'projects' : projects})
    
@login_required(login_url='/login/')
def events(request):
    events = Event.objects.values()
    template = loader.get_template('reference/events.html')
    context = RequestContext( request, {
        'events' : events,
    })
    output = ', '.join([e.get('eventname') for e in events])
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')    
def createEvent(request):
    if request.POST:  #inserts new event into database
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/events/')
    else:
        form = EventForm()
    return render(request, 'reference/createEvent.html', {'form' : form})
  
#########################################################################################
#   END OF FUNCTIONS FOR EVENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PARAMETERS #
#########################################################################################

@login_required(login_url='/login/')
def parameters(request):
    parameters = Parameter.objects.values()
    template = loader.get_template('reference/parameters.html')
    context = RequestContext( request, {
        'parameters' : parameters,
    })
    output = ', '.join([p.get('commonname') for p in parameters])
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def paramDetail(request, param_id):
    param = get_object_or_404(Parameter, pk=param_id)
    return render(request, 'reference/paramDetail.html', {'param' : param})
    
@login_required(login_url='/login/')
def createParam(request):
    if request.POST:
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/parameters/')
    else:
        form = ParamForm()
    return render(request, 'reference/createParam.html', {'form' : form})
    
#########################################################################################
#   END OF FUNCTIONS FOR PARAMETERS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PROJECTS #
#########################################################################################

@login_required(login_url='/login/')
def projects(request):
    projects = Project.objects.values()
    template = loader.get_template('reference/projects.html')
    context = RequestContext( request, {
        'projects' : projects,
    })
    output = ', '.join([p.get('projectname') for p in projects])
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
def projectDetail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    person = get_object_or_404(People, pk=project.personid.objectid)
    event = get_object_or_404(Event, pk=project.eventid.objectid)
    return render(request, 'reference/projectDetail.html', {'project' : project, 'person' : person, 'event' : event})
    
@login_required(login_url='/login/')
def createProject(request):
    if request.POST:  #inserts new project into database
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/projects/')
    else:
        form = ProjectForm()
    return render(request, 'reference/createProject.html', {'form':form})
    
#########################################################################################
#   END OF FUNCTIONS FOR PROJECTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PERMITS #
#########################################################################################

@login_required(login_url='/login/')
def permits(request):
    permits = Permit.objects.values()
    template = loader.get_template('reference/permits.html')
    context = RequestContext( request, {
        'permits' : permits,
    })
    output = ', '.join([str(p.get('id')) for p in permits])
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
def permitDetail(request, permit_id):
    permit = get_object_or_404(Permit, pk=permit_id)
    return render(request, 'reference/permitDetail.html', {'permit' : permit})

@login_required(login_url='/login/')
def createPermit(request):
    if request.POST:
        form = PermitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/permits/')
    else:
        form = PermitForm()
    return render(request, 'reference/createPermit.html', {'form' : form})

#########################################################################################
#   END OF FUNCTIONS FOR PERMITS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR ... #
#########################################################################################
