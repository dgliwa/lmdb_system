from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from lmdb.models import Event, Project, Parameter, Project, Permit, People, Location, Organism, Sighting, Measurement, Change, Collection

from django.db import connection, transaction

from django.http import *
from django.shortcuts import render_to_response,redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib.auth import authenticate, login, logout

from forms import ParamForm, PermitForm, EventForm, ProjectForm, LocationForm, OrganismForm, MeasurementForm, SightingForm, CollectionForm, ChangeForm
import json

@login_required(login_url='/login/')
def index(request):
    
    return render(request,'lmdb/index.html',{})

@login_required(login_url='/login/')
def reference(request):
    
    return render(request,'lmdb/reference.html',{})

@login_required(login_url='/login/')
def data(request):
    
    return render(request,'lmdb/data.html',{})



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
        form.initial['objectid'] = Event.objects.all().order_by('-objectid')[0].objectid+1
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
        form.initial['objectid'] = Parameter.objects.all().order_by('-objectid')[0].objectid+1
    return render(request, 'lmdb/createParam.html', {'form' : form})


@login_required(login_url='/login/')
def createParamFromData(request):
    if request.POST:
        param = Parameter(objectid = Parameter.objects.all().order_by('-objectid')[0].objectid+1)
        param.sciname = request.POST['sciname']
        param.commonname = request.POST['commonname']
        param.casnumber = request.POST['casnumber']
        param.epanumber = request.POST['epanumber']
        param.save()
        return HttpResponse(json.dumps({'id': param.objectid, 'commonname' : param.commonname}))
    return HttpResponse('failed')
    
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
    sightings = Sighting.objects.filter(projectid=project_id)
    changes = Change.objects.filter(projectid=project_id)
    measurements = Measurement.objects.filter(projectid=project_id)
    collections = Collection.objects.filter(projectid=project_id)
    return render(request, 'lmdb/projectDetail.html', {'project' : project, 'person' : person, 'event' : event, 'sightings' : sightings, 'changes' : changes, 'measurements' : measurements, 'collections' : collections})
    
@login_required(login_url='/login/')
def createProject(request):
    if request.POST:  #inserts new project into database
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/reference/projects/')
    else:
        form = ProjectForm()
        form.initial['objectid'] = Project.objects.all().order_by('-objectid')[0].objectid+1
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
        form.initial['objectid'] = Permit.objects.all().order_by('-objectid')[0].objectid+1
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


@login_required(login_url='/login/')
def createLocationPopUp(request):
    if request.POST:
        print request.POST['objectid']
        if request.POST.has_key('indicator'):
            l = Location(objectid = request.POST['objectid'])
            if request.POST['type'] == 'point':
                l.pointid = request.POST['objectid']
            if request.POST['type'] == 'line':
                l.lineid = request.POST['objectid']
            if request.POST['type'] == 'poly':
                l.areaid = request.POST['objectid']
            l.name = request.user.first_name + ' ' + request.user.last_name + ' location'
            l.description = 'Location created during data input'
            print l.save()             
            message = 'Success'
            return render(request, 'lmdb/createLocationPopUp.html', {'message' : message})
    else:
        return HttpResponseRedirect('/lmdb/reference/locations/')

##  !!!! Need to add a sync locations view to allow for locations not tagged to be added to the db !!!! ##

#########################################################################################
#   END OF FUNCTIONS FOR LOCATIONS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR ORGANISMS #
#########################################################################################

@login_required(login_url='/login/')
def organisms(request):
    organisms = Organism.objects.all().order_by('organismname')
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
        form.initial['objectid'] = Organism.objects.all().order_by('-objectid')[0].objectid+1
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
#   END OF FUNCTIONS FOR ORGANISMS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR SIGHTINGS #
#########################################################################################

def sightings(request):    # !!!!!!   NEED TO APPLY FKEY RESTRAINTS
    sightings = Sighting.objects.values()
    points = []
    lines = []
    polys = []
    for s in sightings:
        location = Location.objects.get(pk = s['locationid'])
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)


    template = loader.get_template('lmdb/sightings.html')
    context = RequestContext( request, {
        'sightings' : sightings,
        'points': points,
        'lines': lines,
        'polys': polys,

    })
    return HttpResponse(template.render(context))

def sightingDetail(request, sight_id):
    sighting = get_object_or_404(Sighting, pk=sight_id)
    organism = get_object_or_404(Organism, pk=sighting.organismid.objectid)
    location = get_object_or_404(Location, pk=sighting.locationid)
    project = get_object_or_404(Project, pk=sighting.projectid.objectid)
    person =get_object_or_404(People, pk=sighting.personid.objectid)
    return render(request, 'lmdb/sightingDetail.html', {'person': person, 'project' : project,'sighting' : sighting, 'organism' : organism, 'location' : location})


def createSighting(request):
    if request.POST:
        form = SightingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/data/sightings/')
    else:
        form = SightingForm()
        form.initial['objectid'] = Sighting.objects.all().order_by('-objectid')[0].objectid+1
    points = []
    lines = []
    polys = []
    locations = Location.objects.values()
    for location in locations:
        if location['pointid'] != None:
            points.append(location['pointid'])
        elif location['lineid'] != None:
            lines.append(location['lineid'])
        elif location['areaid'] != None:
            polys.append(location['areaid'])

    return render(request, 'lmdb/createSighting.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})



#########################################################################################
#   END OF FUNCTIONS FOR SIGHTINGS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR CHANGES #
#########################################################################################
def changes(request):     # !!!!!!   NEED TO APPLY FKEY RESTRAINTS
    changes = Change.objects.values()
    points = []
    lines = []
    polys = []
    for c in changes:
        location = Location.objects.get(pk = c['locationid'])
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)

    template = loader.get_template('lmdb/changes.html')
    context = RequestContext( request, {
        'changes' : changes,
        'points': points,
        'lines': lines,
        'polys': polys,

    })
    return HttpResponse(template.render(context))

def changeDetail(request, change_id):
    change = get_object_or_404(Change, pk=change_id)
    parameter = get_object_or_404(Parameter, pk=change.parameterid.objectid)
    location = get_object_or_404(Location, pk=change.locationid)
    project = get_object_or_404(Project, pk=change.projectid.objectid)
    person =get_object_or_404(People, pk=change.personid.objectid)
    return render(request, 'lmdb/changeDetail.html', {'person': person, 'project' : project,'change' : change, 'parameter' : parameter, 'location' : location})


def createChange(request):
    if request.POST:
        form = ChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/data/changes/')
    else:
        form = ChangeForm()
        form.initial['objectid'] = Change.objects.all().order_by('-objectid')[0].objectid+1
    points = []
    lines = []
    polys = []
    locations = Location.objects.values()
    for location in locations:
        if location['pointid'] != None:
            points.append(location['pointid'])
        elif location['lineid'] != None:
            lines.append(location['lineid'])
        elif location['areaid'] != None:
            polys.append(location['areaid'])

    return render(request, 'lmdb/createChange.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})


#########################################################################################
#   END OF FUNCTIONS FOR CHANGES #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR MEASUREMENTS #
#########################################################################################
def measurements(request):
    measurements = Measurement.objects.values()
    points = []
    lines = []
    polys = []
    for m in measurements:
        location = Location.objects.get(pk = m['locationid'])
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)
    template = loader.get_template('lmdb/measurements.html')
    context = RequestContext( request, {
        'measurements' : measurements,
        'points': points,
        'lines': lines,
        'polys': polys,
    })
    return HttpResponse(template.render(context))


def measurementDetail(request, meas_id):
    measurement = get_object_or_404(Measurement, pk=meas_id)
    parameter = get_object_or_404(Parameter, pk=measurement.parameterid.objectid)
    location = get_object_or_404(Location, pk=measurement.locationid)
    project = get_object_or_404(Project, pk=measurement.projectid.objectid)
    person =get_object_or_404(People, pk=measurement.personid.objectid)
    return render(request, 'lmdb/measurementDetail.html', {'person': person, 'project' : project,'measurement' : measurement, 'parameter' : parameter, 'location' : location})

def createMeasurement(request):
    if request.POST:
        form = MeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/data/measurements/')
    else:
        form = MeasurementForm()
        form.initial['objectid'] = Measurement.objects.all().order_by('-objectid')[0].objectid+1
    points = []
    lines = []
    polys = []
    locations = Location.objects.values()
    for location in locations:
        if location['pointid'] != None:
            points.append(location['pointid'])
        elif location['lineid'] != None:
            lines.append(location['lineid'])
        elif location['areaid'] != None:
            polys.append(location['areaid'])

    return render(request, 'lmdb/createMeasurement.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})



#########################################################################################
#   END OF FUNCTIONS FOR MEASUREMENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR COLLECTIONS #
#########################################################################################
def collections(request):    # !!!!!!   NEED TO APPLY FKEY RESTRAINTS
    collections = Collection.objects.values()
    points = []
    lines = []
    polys = []
    for c in collections:
        location = Location.objects.get(pk = c['locationid'])
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)


    template = loader.get_template('lmdb/collections.html')
    context = RequestContext( request, {
        'collections' : collections,
        'points': points,
        'lines': lines,
        'polys': polys,

    })
    return HttpResponse(template.render(context))


def collectionDetail(request, coll_id):
    collection = get_object_or_404(Collection, pk=coll_id)
    organism = get_object_or_404(Organism, pk=collection.organismid.objectid)
    location = get_object_or_404(Location, pk=collection.locationid)
    project = get_object_or_404(Project, pk=collection.projectid.objectid)
    person =get_object_or_404(People, pk=collection.personid.objectid)
    return render(request, 'lmdb/collectionDetail.html', {'person': person, 'project' : project,'collection' : collection, 'organism' : organism, 'location' : location})
    

def createCollection(request):
    if request.POST:
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lmdb/data/collections/')
    else:
        form = CollectionForm()
        form.initial['objectid'] = Collection.objects.all().order_by('-objectid')[0].objectid+1
    points = []
    lines = []
    polys = []
    locations = Location.objects.values()
    for location in locations:
        if location['pointid'] != None:
            points.append(location['pointid'])
        elif location['lineid'] != None:
            lines.append(location['lineid'])
        elif location['areaid'] != None:
            polys.append(location['areaid'])

    return render(request, 'lmdb/createCollection.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})




#########################################################################################
#   END OF FUNCTIONS FOR COLLECTIONS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR LOGIN INFORMATION #
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