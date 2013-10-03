from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from lmdb.models import Event, Project, Parameter, Project, Permit, People, Location, Organism

from django.db import connection, transaction

from django.http import *
from django.shortcuts import render_to_response,redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib.auth import authenticate, login, logout

from forms import ParamForm, PermitForm, EventForm, ProjectForm, LocationForm, OrganismForm
import json

@login_required(login_url='/login/')
def index(request):
    
    return render(request,'lmdb/index.html',{})

@login_required(login_url='/login/')
def reference(request):
    
    return render(request,'lmdb/reference.html',{})


#########################################################################################
#   BEGINNING OF FUNCTIONS FOR EVENTS #
#########################################################################################
    
@login_required(login_url='/login/')
def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    person = get_object_or_404(People, pk=event.personid.objectid)
    projects = Project.objects.get_query_set().filter(eventid=event.objectid)
    return render(request, 'lmdb/eventDetail.html', {'event' : event, 'person' : person, 'projects' : projects})
    
@login_required(login_url='/login/')
def events(request):
    events = Event.objects.values()
    template = loader.get_template('lmdb/events.html')
    context = RequestContext( request, {
        'events' : events,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')    
def createEvent(request):
    if request.POST:  #inserts new event into database
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/events/')
    else:
        form = EventForm()
    return render(request, 'lmdb/createEvent.html', {'form' : form})
  
#########################################################################################
#   END OF FUNCTIONS FOR EVENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PARAMETERS #
#########################################################################################

@login_required(login_url='/login/')
def parameters(request):
    parameters = Parameter.objects.values()
    template = loader.get_template('lmdb/parameters.html')
    context = RequestContext( request, {
        'parameters' : parameters,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def paramDetail(request, param_id):
    param = get_object_or_404(Parameter, pk=param_id)
    return render(request, 'lmdb/paramDetail.html', {'param' : param})
    
@login_required(login_url='/login/')
def createParam(request):
    if request.POST:
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/parameters/')
    else:
        form = ParamForm()
    return render(request, 'lmdb/createParam.html', {'form' : form})
    
#########################################################################################
#   END OF FUNCTIONS FOR PARAMETERS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PROJECTS #
#########################################################################################

@login_required(login_url='/login/')
def projects(request):
    projects = Project.objects.values()
    template = loader.get_template('lmdb/projects.html')
    context = RequestContext( request, {
        'projects' : projects,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
def projectDetail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    person = get_object_or_404(People, pk=project.personid.objectid)
    event = get_object_or_404(Event, pk=project.eventid.objectid)
    return render(request, 'lmdb/projectDetail.html', {'project' : project, 'person' : person, 'event' : event})
    
@login_required(login_url='/login/')
def createProject(request):
    if request.POST:  #inserts new project into database
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/projects/')
    else:
        form = ProjectForm()
    return render(request, 'lmdb/createProject.html', {'form':form})
    
#########################################################################################
#   END OF FUNCTIONS FOR PROJECTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PERMITS #
#########################################################################################

@login_required(login_url='/login/')
def permits(request):
    permits = Permit.objects.values()
    template = loader.get_template('lmdb/permits.html')
    context = RequestContext( request, {
        'permits' : permits,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
def permitDetail(request, permit_id):
    permit = get_object_or_404(Permit, pk=permit_id)
    return render(request, 'lmdb/permitDetail.html', {'permit' : permit})

@login_required(login_url='/login/')
def createPermit(request):
    if request.POST:
        form = PermitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/permits/')
    else:
        form = PermitForm()
    return render(request, 'lmdb/createPermit.html', {'form' : form})

#########################################################################################
#   END OF FUNCTIONS FOR PERMITS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR LOCATIONS #
#########################################################################################

@login_required(login_url='/login/')
def locations(request):
    locations = Location.objects.all().order_by('pointid','lineid','areaid')
    template = loader.get_template('lmdb/locations.html')
    context = RequestContext( request, {
        'locations' : locations,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
def locationDetail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'lmdb/locationDetail.html', {'location' : location})

@login_required(login_url='/login/')
def createLocationMap(request):
        return render(request,'lmdb/createLocationMap.html',{})
    
    
@login_required(login_url='/login/')
@csrf_exempt
def createLocation(request):

    @csrf_protect
    def formValidation(request):
        if request.POST:
            form = LocationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/lmdb/reference/locations/')
        else:
            form = LocationForm()
        return render(request, 'lmdb/createLocation.html', {'form': form})    

    if request.POST:
        print request.POST['objectid']
        if request.POST.has_key('indicator'):
            form = LocationForm()
            form.initial['objectid'] = request.POST['objectid']
            if request.POST['type'] == 'point':
                form.initial['pointid'] = request.POST['objectid']
            if request.POST['type'] == 'line':
                form.initial['lineid'] = request.POST['objectid']
            if request.POST['type'] == 'poly':
                form.initial['areaid'] = request.POST['objectid']
            return render(request, 'lmdb/createLocation.html', {'form' : form})
        else:
            return formValidation(request)
    else:
        return HttpResponseRedirect('/lmdb/reference/locations/create/map/')

##  !!!! Need to add a sync locations view to allow for locations not tagged to be added to the db !!!! ##

#########################################################################################
#   END OF FUNCTIONS FOR LOCATIONS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR ORGANISMS #
#########################################################################################

@login_required(login_url='/login/')
def organisms(request):
    organisms = Organism.objects.all().order_by('kingdom')
    template = loader.get_template('lmdb/organisms.html')
    context = RequestContext( request, {
        'organisms' : organisms,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')   
def organismDetail(request, org_id):
    organism = get_object_or_404(Organism, pk=org_id)
    return render(request, 'lmdb/organismDetail.html', {'organism' : organism})

@login_required(login_url='/login/')
def createOrganism(request):
    if request.POST:
        form = OrganismForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/organisms/')
    else:
        form = OrganismForm()
    return render(request, 'lmdb/createOrganism.html', {'form' : form})

#########################################################################################
# FUNCTIONS THAT HANDLE AJAX CALLS FROM THE CREATE ORGANISMS PAGE  #
def kingdomFilter(request, king_id):
	from django.core import serializers
	b = Organism.objects.filter(kingdom=king_id).values('phylum').distinct()  
	data = json.dumps([dict(phylum = org['phylum']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")
	
def phylumFilter(request, phyl_id):
	from django.core import serializers
	b = Organism.objects.filter(phylum=phyl_id).values('class_field').distinct()  
	data = json.dumps([dict(class_field = org['class_field']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

def classFilter(request, class_id):
	from django.core import serializers
	b = Organism.objects.filter(class_field=class_id).values('order_field').distinct()  
	data = json.dumps([dict(order_field = org['order_field']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")
	
def orderFilter(request, order_id):
	from django.core import serializers
	b = Organism.objects.filter(order_field=order_id).values('family').distinct()  
	data = json.dumps([dict(family = org['family']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

def familyFilter(request, family_id):
	from django.core import serializers
	b = Organism.objects.filter(family=family_id).values('genus').distinct()  
	data = json.dumps([dict(genus = org['genus']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")
	
#########################################################################################




from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


###logout(request) 

#handles the logins of users and holds home page

@login_required(login_url='/login/')
def index(request):
    return render(request,'lmdb/index.html',{})


def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/lmdb/')
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/lmdb/')
    return render_to_response('login.html', context_instance=RequestContext(request))
    
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/lmdb/login')