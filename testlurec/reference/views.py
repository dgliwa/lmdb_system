from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from reference.models import Event, AuthUser, Project, Parameter

from django.http import *
from django.shortcuts import render_to_response,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import random #will be removed later, need to update database


@login_required(login_url='/login/')
def index(request):
    
    return render(request,'reference/reference.html',{})


#########################################################################################
#   BEGINNING OF FUNCTIONS FOR EVENTS #
    
@login_required(login_url='/login/')
def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    person = get_object_or_404(AuthUser, pk=event.personid)
    projects = Project.objects.get_query_set().filter(eventid=event.id)
    return render(request, 'reference/eventDetail.html', {'event' : event, 'person' : person, 'projects' : projects})
    
@login_required(login_url='/login/')
def events(request):
    if request.POST:  #inserts new event into database
        e = Event(objectid=random.randint(1,10000), eventname=request.POST['eventname'], eventtype=request.POST['eventtype'], eventstartdate=request.POST['eventstartdate'], eventenddate=request.POST['eventenddate'], eventparticipants=request.POST['eventparticipants'], eventdescription=request.POST['eventdescription'], personid=request.POST['personid'])
        e.save()
        return HttpResponseRedirect('/reference/events/')
    events = Event.objects.values()
    template = loader.get_template('reference/events.html')
    context = RequestContext( request, {
        'events' : events,
    })
    output = ', '.join([e.get('eventname') for e in events])
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')    
def createEvent(request):
    people = AuthUser.objects.values()
    return render(request, 'reference/createEvent.html', {'people' : people})
  
#########################################################################################
#   END OF FUNCTIONS FOR EVENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PARAMETERS #

@login_required(login_url='/login/')
def parameters(request):
    if request.POST:
        p = Parameter(objectid=random.randint(1,10000), sciname=request.POST['sciname'], commonname=request.POST['commonname'], casnumber=request.POST['casnumber'], epanumber=request.POST['epanumber'])
        p.save()
        return HttpResponseRedirect('/reference/parameters/')
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
    people = AuthUser.objects.values()
    return render(request, 'reference/createParam.html', {'people' : people})