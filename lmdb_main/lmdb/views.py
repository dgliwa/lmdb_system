from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from lmdb.models import *

from django.http import *
from django.shortcuts import render_to_response,redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import permission_required
from lmdb.decorators import user_uploaded 
from django.contrib.auth.forms import PasswordChangeForm

from forms import *
import json

@login_required(login_url='/login/')
@user_uploaded
def index(request):
    print request.user
    id = request.user.id
    person = People.objects.get(objectid=id)
    projects = Project.objects.get_query_set().filter(personid=person)
    return render(request,'lmdb/index.html',{'projects':projects})

@login_required(login_url='/login/')
@user_uploaded
def reference(request):
    return render(request,'lmdb/reference.html',{})


#########################################################################################
#   USER MANAGEMENT #
#########################################################################################
@login_required(login_url='/login/')
def updateUser(request):
    try:
        p = People.objects.get(objectid=request.user.id)
    except People.DoesNotExist:
        #u = User.objects.get(pk = request.user.id)
        p = People(objectid=request.user.id, firstname=request.user.first_name,lastname=request.user.last_name)
        p.save()
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = request.user.id
        if request.user.first_name:
            postVals['firstname'] = request.user.first_name
        else:
            u = User.objects.get(pk = request.user.id)
            u.first_name = postVals['firstname']
            u.save()
        if request.user.last_name:
            postVals['lastname'] = request.user.last_name
        else:
            u = User.objects.get(pk = request.user.id)
            u.last_name = postVals['lastname']
            u.save()
        if request.user.email:
            postVals['email'] = request.user.email
        else:
            u = User.objects.get(pk = request.user.id)
            u.email = postVals['email']
            u.save()

        form = PeopleForm(postVals, instance = p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:   
        updater = request.user
        person = User.objects.get(id = updater.id)
        form = PeopleForm(instance=p)
        
    return render(request,'lmdb/updateUser.html',{'form' : form})

@login_required(login_url='/login/')
@user_uploaded
def passwordreset(request):
    form = PasswordChangeForm(user=request.user)
    print form
    if request.POST:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        print form.is_valid()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/updateUser/')
    return render(request, 'passwordreset.html',{'form':form})
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR EVENTS #
#########################################################################################
    
@login_required(login_url='/login/')
@user_uploaded
def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    person = get_object_or_404(People, pk=event.personid.objectid)
    projects = Project.objects.get_query_set().filter(eventid=event.objectid)
    return render(request, 'lmdb/eventDetail.html', {'event' : event, 'person' : person, 'projects' : projects})


@login_required(login_url='/login/')
@user_uploaded
def events(request):
    events = Event.objects.values()
    template = loader.get_template('lmdb/events.html')
    context = RequestContext( request, {
        'events' : events,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
@user_uploaded
@permission_required('events.can_add', raise_exception=True)    
def createEvent(request):
    if request.POST:  #inserts new event into database
        postVals = request.POST.copy()
        postVals['objectid'] = Event.objects.all().order_by('-objectid')[0].objectid+1
        form = EventForm(postVals)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/events/')
    else:
        form = EventForm()
        form.initial['objectid'] = 1
    return render(request, 'lmdb/createEvent.html', {'form' : form})

@login_required(login_url='/login/')
@user_uploaded
def editEvent(request, event_id):
    event = Event.objects.get(objectid=event_id)    
    if request.POST:
        form = EventForm(request.POST, instance = event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/events/'+ event_id + '/')
    else:
        form = EventForm(instance=event)
    return render(request, 'lmdb/editEvent.html', {'form':form, 'event':event})
  
#########################################################################################
#   END OF FUNCTIONS FOR EVENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PARAMETERS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
def parameters(request):
    parameters = Parameter.objects.values()
    template = loader.get_template('lmdb/parameters.html')
    context = RequestContext( request, {
        'parameters' : parameters,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
@user_uploaded
def paramDetail(request, param_id):
    param = get_object_or_404(Parameter, pk=param_id)
    return render(request, 'lmdb/paramDetail.html', {'param' : param})
    
@login_required(login_url='/login/')
@user_uploaded
def createParam(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Parameter.objects.all().order_by('-objectid')[0].objectid+1
        form = ParamForm(postVals)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/parameters/')
    else:
        form = ParamForm()
        form.initial['objectid'] = 1
    return render(request, 'lmdb/createParam.html', {'form' : form})


@login_required(login_url='/login/')
@user_uploaded
def editParam(request, param_id):
    param = Parameter.objects.get(objectid=param_id)    
    if request.POST:
        form = ParamForm(request.POST, instance = param)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/parameters/'+ param_id + '/')
    else:
        form = ParamForm(instance=param)
    return render(request, 'lmdb/editParam.html', {'form':form, 'param':param})
 

@login_required(login_url='/login/')
@user_uploaded
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
@user_uploaded
def projects(request):
    projects = Project.objects.values()
    template = loader.get_template('lmdb/projects.html')
    context = RequestContext( request, {
        'projects' : projects,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
@user_uploaded
def projectDetail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    person = get_object_or_404(People, pk=project.personid.objectid)
    event = get_object_or_404(Event, pk=project.eventid.objectid)
    sightings = Sighting.objects.filter(projectid=project_id)
    changes = Change.objects.filter(projectid=project_id)
    measurements = Measurement.objects.filter(projectid=project_id)
    collections = Collection.objects.filter(projectid=project_id)
    peopleprojects = PeopleProject.objects.filter(projectid=project)
    people = []
    for p in peopleprojects:
        people.append(People.objects.get(objectid=p.personid.objectid))
    return render(request, 'lmdb/projectDetail.html', {'project' : project, 'person' : person, 'event' : event, 'sightings' : sightings, 'changes' : changes, 'measurements' : measurements, 'collections' : collections, 'people' : people})
    
@login_required(login_url='/login/')
@user_uploaded
def createProject(request):
    if request.POST:  #inserts new project into database
        postVals = request.POST.copy()
        postVals['objectid'] = Project.objects.all().order_by('-objectid')[0].objectid+1
        form = ProjectForm(postVals)
        if form.is_valid():
                form.save()
        project = Project.objects.get(objectid=postVals['objectid'])
        if postVals['post'] == 'yes':            
            people = postVals['people'].split(',')
            for person in people:
                p = People.objects.get(objectid=int(person))
                if PeopleProject.objects.count() == 0:
                    pp = PeopleProject(objectid=1)
                else:
                    pp = PeopleProject(objectid = PeopleProject.objects.all().order_by('-objectid')[0].objectid+1)
                pp.personid = p
                pp.projectid = project
                print pp
                pp.save()
            if PeopleProject.objects.count() == 0:
                pp = PeopleProject(objectid=1)
            else:
                pp = PeopleProject(objectid = PeopleProject.objects.all().order_by('-objectid')[0].objectid+1)
            pp.personid = request.user.id
            pp.projectid = project
            print pp
            pp.save()
            return HttpResponseRedirect('/reference/projects/')
        else:
            if PeopleProject.objects.count() == 0:
                pp = PeopleProject(objectid=1)
            else:
                pp = PeopleProject(objectid = PeopleProject.objects.all().order_by('-objectid')[0].objectid+1)
            pp.personid = People.objects.get(objectid=request.user.id)
            pp.projectid = project
            pp.save()
            return HttpResponseRedirect('/reference/projects/')
    else:
        form = ProjectForm()
        form.initial['objectid'] = 1
    people = People.objects.get_query_set().exclude(objectid=request.user.id)
    return render(request, 'lmdb/createProject.html', {'form':form, 'people':people})


@login_required(login_url='/login/')
@user_uploaded
def editProject(request, project_id):
    project = Project.objects.get(objectid=project_id)    
    if request.POST:
        form = ProjectForm(request.POST, instance = project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/projects/'+ project_id + '/')
    else:
        form = ProjectForm(instance=project)
    peopleprojects = PeopleProject.objects.filter(projectid=project)
    people = []
    for p in peopleprojects:
        people.append(People.objects.get(objectid=p.personid.objectid))
    if len(people)==0:
        people = None
    return render(request, 'lmdb/editProject.html', {'form':form, 'people':people, 'project' : project})

@login_required(login_url='/login/')
@user_uploaded
def addProjectPeople(request, project_id):
    if request.POST:
        dict = request.POST
        vals = dict.keys()
        for val in vals:
            if val != 'csrfmiddlewaretoken':
                if PeopleProject.objects.count() == 0:
                    pp = PeopleProject(objectid=1)
                else:
                    pp = PeopleProject(objectid = PeopleProject.objects.all().order_by('-objectid')[0].objectid+1)
                pp.personid = People.objects.get(objectid = dict[val])
                pp.projectid = Project.objects.get(objectid = project_id)
                pp.save()
        return HttpResponseRedirect('/reference/projects/' + project_id + '/edit/')
    project= Project.objects.get(objectid=project_id)
    peopleprojects = PeopleProject.objects.filter(projectid=project)
    people = People.objects.get_query_set().exclude(objectid=request.user.id)
    for p in peopleprojects:
        people = people.exclude(objectid=p.personid.objectid)
    return render(request, 'lmdb/addProjectPeople.html', {'people':people, 'pid' : project_id})

@login_required(login_url='/login/')
@user_uploaded
def removeProjectPeople(request, project_id):
    if request.POST:
        dict = request.POST
        vals = dict.keys()
        project = Project.objects.get(objectid=project_id)
        for val in vals:
            if val != 'csrfmiddlewaretoken':
                person = People.objects.get(objectid = dict[val])
                pp = PeopleProject.objects.filter(projectid = project)
                assigned = pp.filter(personid = person)
                assigned.delete()
        return HttpResponseRedirect('/reference/projects/' + project_id + '/edit/')
    else:
        project = Project.objects.get(objectid=project_id)
        peopleproject = PeopleProject.objects.filter(projectid=project)
        people = []
        for pp in peopleproject:
            people.append(People.objects.get(objectid=pp.personid.objectid))
    return render(request, 'lmdb/removeProjectPeople.html', {'people':people, 'pid' : project_id})
    
#########################################################################################
#   END OF FUNCTIONS FOR PROJECTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR PERMITS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
def permits(request):
    permits = Permit.objects.values()
    template = loader.get_template('lmdb/permits.html')
    context = RequestContext( request, {
        'permits' : permits,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
@user_uploaded
def permitDetail(request, permit_id):
    permit = get_object_or_404(Permit, pk=permit_id)
    print permit
    projects = Project.objects.filter(permitid=permit)
    return render(request, 'lmdb/permitDetail.html', {'permit' : permit, 'projects' : projects})

@login_required(login_url='/login/')
@user_uploaded
def createPermit(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Permit.objects.all().order_by('-objectid')[0].objectid+1
        form = PermitForm(postVals)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/permits/')
    else:
        form = PermitForm()
        form.initial['objectid'] = 1
    return render(request, 'lmdb/createPermit.html', {'form' : form})

@login_required(login_url='/login/')
@user_uploaded
def editPermit(request, permit_id):
    permit = Permit.objects.get(objectid=permit_id)    
    if request.POST:
        form = PermitForm(request.POST, instance = permit)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/permits/'+ permit_id + '/')
    else:
        form = PermitForm(instance=permit)
    return render(request, 'lmdb/editParam.html', {'form':form, 'permit':permit})

#########################################################################################
#   END OF FUNCTIONS FOR PERMITS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR LOCATIONS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
def locations(request):
    locations = Location.objects.all().order_by('pointid','lineid','areaid')
    template = loader.get_template('lmdb/locations.html')
    context = RequestContext( request, {
        'locations' : locations,
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login/')
@user_uploaded
def locationDetail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'lmdb/locationDetail.html', {'location' : location})

@login_required(login_url='/login/')
@user_uploaded
def createLocationMap(request):
        return render(request,'lmdb/createLocationMap.html',{})
    
    
@login_required(login_url='/login/')
@user_uploaded
@csrf_exempt
def createLocation(request):

    @csrf_protect
    def formValidation(request):
        if request.POST:
            form = LocationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/reference/locations/')
        else:
            form = LocationForm()
        return render(request, 'lmdb/createLocation.html', {'form': form})    

    if request.POST:
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
        return HttpResponseRedirect('/reference/locations/create/map/')

@login_required(login_url='/login/')
@user_uploaded
def createLocationPopUp(request):
    if request.POST:
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
        return HttpResponseRedirect('/reference/locations/')

@login_required(login_url='/login/')
@user_uploaded
@permission_required('locations.can_add', raise_exception=True)    
@permission_required('locations.can_delete', raise_exception=True)    
def locationCleanup(request):
    locations = Location.objects.values()
    points = []
    lines = []
    polys = []
    for location in locations: 
        if location['pointid'] != None:
            points.append(location['pointid'])
        elif location['lineid'] != None:
            lines.append(location['lineid'])
        elif location['areaid'] != None:
            polys.append(location['areaid'])

    return render(request, 'lmdb/locationCleanup.html', {'points':points, 'lines':lines,'polys':polys})


@login_required(login_url='/login/')
@user_uploaded
def editLocation(request, location_id):
    location = Location.objects.get(objectid=location_id)    
    if request.POST:
        form = LocationForm(request.POST, instance = location)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/locations/'+ location_id + '/')
    else:
        form = LocationForm(instance=location)
    return render(request, 'lmdb/editLocation.html', {'form':form, 'location':location})

##  !!!! Need to add a sync locations view to allow for locations not tagged to be added to the db !!!! ##

#########################################################################################
#   END OF FUNCTIONS FOR LOCATIONS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR ORGANISMS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
def organisms(request):
    organisms = Organism.objects.all().order_by('organismname')
    template = loader.get_template('lmdb/organisms.html')
    context = RequestContext( request, {
        'organisms' : organisms,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
@user_uploaded   
def organismDetail(request, org_id):
    organism = get_object_or_404(Organism, pk=org_id)
    collections = Collection.objects.filter(organismid=organism)
    sightings = Sighting.objects.filter(organismid=organism)
    return render(request, 'lmdb/organismDetail.html', {'organism' : organism, 'collections':collections, 'sightings':sightings})

@login_required(login_url='/login/')
@user_uploaded
def createOrganism(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Organism.objects.all().order_by('-objectid')[0].objectid+1
        form = OrganismForm(postVals)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/organisms/')
    else:
        form = OrganismForm()
        form.initial['objectid'] = 1
    return render(request, 'lmdb/createOrganism.html', {'form' : form})
    
@login_required(login_url='/login/')
def createOrganismFromData(request):
    if request.POST:
        org = Organism(objectid = Organism.objects.all().order_by('-objectid')[0].objectid+1)
        org.organismname = request.POST['organismname']
        org.kingdom = request.POST['kingdom']
        
        org.phylum = request.POST['phylum']
        org.class_field = request.POST['class_field']
        org.order_field = request.POST['order_field']
        org.family = request.POST['family']
        org.genus = request.POST['genus']
        org.species = request.POST['species']
        if request.POST['wetland_designation'] != '':
            org.wetland_designation = request.POST['wetland_designation']
        if request.POST['cvalue'] != '':
            org.cvalue = request.POST['cvalue']
        if request.POST.has_key('introduced'):
            org.introduced = request.POST['introduced']
        org.save()
        return HttpResponse(json.dumps({'id': org.objectid, 'organismname' : org.organismname}))
    return HttpResponse('failed')

@login_required(login_url='/login/')
@user_uploaded
def editOrganism(request, org_id):
    organism = Organism.objects.get(objectid=org_id)
    print organism    
    if request.POST:
        form = EditOrganismForm(request.POST, instance = organism)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reference/organisms/'+ org_id + '/')
    else:
        form = EditOrganismForm(instance=organism)
    return render(request, 'lmdb/editOrganism.html', {'form':form, 'organism':organism})

#########################################################################################
# FUNCTIONS THAT HANDLE AJAX CALLS FROM THE CREATE ORGANISMS PAGE  #
@login_required(login_url='/login/')
def kingdomFilter(request, king_id):
	from django.core import serializers
	b = Organism.objects.filter(kingdom=king_id).values('phylum').distinct()  
	data = json.dumps([dict(phylum = org['phylum']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')	
def phylumFilter(request, phyl_id):
	from django.core import serializers
	b = Organism.objects.filter(phylum=phyl_id).values('class_field').distinct()  
	data = json.dumps([dict(class_field = org['class_field']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')
def classFilter(request, class_id):
	from django.core import serializers
	b = Organism.objects.filter(class_field=class_id).values('order_field').distinct()  
	data = json.dumps([dict(order_field = org['order_field']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')
def plantClassFilter(request, class_id):
    from django.core import serializers
    b = Organism.objects.filter(class_field=class_id).values('family').distinct()  
    data = json.dumps([dict(family = org['family']) for org in b])
    return HttpResponse(data, mimetype="application/javascript")
	
@login_required(login_url='/login/')
def orderFilter(request, order_id):
	from django.core import serializers
	b = Organism.objects.filter(order_field=order_id).values('family').distinct()  
	data = json.dumps([dict(family = org['family']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')
def familyFilter(request, family_id):
	from django.core import serializers
	b = Organism.objects.filter(family=family_id).values('genus').distinct()  
	data = json.dumps([dict(genus = org['genus']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')
def genusFilter(request, genus_id):
	from django.core import serializers
	b = Organism.objects.filter(genus=genus_id).values('organismname','objectid').distinct()  
	data = json.dumps([dict(organismname = org['organismname'], objectid=org['objectid']) for org in b])
	return HttpResponse(data, mimetype="application/javascript")

@login_required(login_url='/login/')
def species(request,column, filter):
    if column=='kingdom':
        b = Organism.objects.filter(kingdom = filter).values('organismname','objectid').distinct()
    elif column=='phylum':
        b = Organism.objects.filter(phylum = filter).values('organismname','objectid').distinct()
    elif column=='order_field':
        b = Organism.objects.filter(order_field = filter).values('organismname','objectid').distinct()
    elif column=='family':
        b = Organism.objects.filter(family = filter).values('organismname','objectid').distinct()
    elif column=='class_field':
        b = Organism.objects.filter(class_field = filter).values('organismname','objectid').distinct()
    elif column=='genus':
        b = Organism.objects.filter(genus = filter).values('organismname','objectid').distinct()
    else:
        return HttpResponse('failed')
    data = json.dumps([dict(organismname = org['organismname'], objectid=org['objectid']) for org in b])
    return HttpResponse(data, mimetype="application/javascript")

@login_required
def organismSelect(request, id):
    return "ok"    
#########################################################################################
#   END OF FUNCTIONS FOR ORGANISMS #
#

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



def login_user(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    username = password = ''
    if request.POST:
        #print request.POST
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(redirect_to)
    return render_to_response('login.html',{'redirect_to':redirect_to}, context_instance=RequestContext(request))
    
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def done(request):
    return render_to_response('done.html',{})
