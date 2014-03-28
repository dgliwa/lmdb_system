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


from forms import *
import json

@login_required(login_url='/login/')
@user_uploaded
def index(request):
    id = request.user.id
    person = People.objects.get(objectid=id)
    projects = Project.objects.get_query_set().filter(personid=person)
    return render(request,'lmdb/index.html',{'projects':projects})

@login_required(login_url='/login/')
@user_uploaded
def reference(request):
    return render(request,'lmdb/reference.html',{})

@login_required(login_url='/login/')
@user_uploaded
def data(request):
    return render(request,'lmdb/data.html',{})

@login_required(login_url='/login/')
@user_uploaded
def dataUpdate(request):
    if request.user.is_staff:
        sightings = Sighting.objects.all()
        measurements = Measurement.objects.all()
        collections = Collection.objects.all()
        changes = Change.objects.all()
    else:
        id = request.user.id
        person = People.objects.get(objectid = id)
        sightings = Sighting.objects.get_query_set().filter(personid = person)
        measurements = Measurement.objects.get_query_set().filter(personid = person)
        collections = Collection.objects.get_query_set().filter(personid = person)
        changes = Change.objects.get_query_set().filter(personid = person)
    return render(request,'lmdb/dataUpdate.html',{'sightings':sightings,'measurements':measurements,'collections':collections,'changes':changes})

@login_required(login_url='/login/')
@user_uploaded
def dataDelete(request):
    if request.POST:
        dict = request.POST
        vals = dict.keys()
        if request.user.is_staff:
            for val in vals:
                if val != 'csrfmiddlewaretoken':
                    split = dict[val].split(',')
                    if split[0] == 'Change':
                        c = Change.objects.get(objectid=int(split[1]))
                        c.delete()
                    elif split[0] == 'Sighting':
                        s = Sighting.objects.get(objectid=int(split[1]))
                        s.delete()
                    elif split[0] == 'Measurement':
                        m = Measurement.objects.get(objectid=int(split[1]))
                        m.delete()
                    elif split[0] == 'Collection':
                        c = Collection.objects.get(objectid=int(split[1]))
                        c.delete()
            sightings = Sighting.objects.all()
            measurements = Measurement.objects.all()
            collections = Collection.objects.all()
            changes = Change.objects.all()
            return HttpResponseRedirect('/data/update/')
        else:
            for val in vals:
                if val != 'csrfmiddlewaretoken':
                    split = dict[val].split(',')
                    if split[0] == 'Change':
                        c = Change.objects.get(objectid=int(split[1]))
                        if request.user.id == c.personid.objectid:
                            c.delete()
                    elif split[0] == 'Sighting':
                        s = Sighting.objects.get(objectid=int(split[1]))
                        if request.user.id == s.personid.objectid:
                            s.delete()
                    elif split[0] == 'Measurement':
                        m = Measurement.objects.get(objectid=int(split[1]))
                        if request.user.id == m.personid.objectid:
                            m.delete()
                    elif split[0] == 'Collection':
                        c = Collection.objects.get(objectid=int(split[1]))
                        if request.user.id == c.personid.objectid:
                            c.delete()
            sightings = Sighting.objects.all()
            measurements = Measurement.objects.all()
            collections = Collection.objects.all()
            changes = Change.objects.all()
            return HttpResponseRedirect('/data/update/')
    return HttpResponseRedirect('/data/update/')

@login_required(login_url='/login/')
@user_uploaded
def dataUpdateForm(request):
    if request.POST:
        changeforms =[]
        sightingforms = []
        measurementforms = []
        collectionforms = []
        dict = request.POST
        vals = dict.keys()
        for val in vals:
            if val != 'csrfmiddlewaretoken':
                split = dict[val].split(',')
                if split[0] == 'Change':
                    c = Change.objects.get(objectid=int(split[1]))
                    form = ChangeForm(instance=c, user=request.user.id)
                    form.initial['projectid'] = c.projectid
                    changeforms.append(form)
                elif split[0] == 'Sighting':
                    s = Sighting.objects.get(objectid=int(split[1]))
                    form = SightingForm(instance=s, user=request.user.id)
                    form.initial['projectid'] = s.projectid
                    sightingforms.append(form)
                elif split[0] == 'Measurement':
                    m = Measurement.objects.get(objectid=int(split[1]))
                    form = MeasurementForm(instance=m, user=request.user.id)
                    form.initial['projectid'] = m.projectid
                    measurementforms.append(form)
                elif split[0] == 'Collection':
                    c = Collection.objects.get(objectid=int(split[1]))
                    form = CollectionForm(instance=c, user=request.user.id)
                    form.initial['projectid'] = c.projectid
                    collectionforms.append(form)
        if len(collectionforms) == 0:
            collectionforms = None
        if len(changeforms) == 0:
            changeforms = None
        if len(measurementforms) == 0:
            measurementforms = None
        if len(sightingforms) == 0:
            sightingforms = None 
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
        
    return render(request,'lmdb/dataUpdateForm.html',{'collectionforms':collectionforms, 'changeforms':changeforms,'measurementforms':measurementforms,'sightingforms':sightingforms, 'points':points, 'lines':lines,'polys':polys})

#########################################################################################
#   USER MANAGEMENT #
#########################################################################################
@login_required(login_url='/login/')
def updateUser(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = request.user.id
        postVals['firstname'] = request.user.first_name
        postVals['lastname'] = request.user.last_name
        form = PeopleForm(postVals)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:   
        updater = request.user
        person = User.objects.get(id = updater.id)
        form = PeopleForm()
        form.initial['objectid'] = updater.id
        form.initial['firstname'] = updater.first_name
        form.initial['lastname'] = updater.last_name
        form.initial['displayname'] = updater.first_name + ' ' + updater.last_name
        form.initial['email'] = updater.email
    return render(request,'lmdb/updateUser.html',{'form' : form})
# @login_required(login_url='/login/')
# @permission_required('users.can_add')
# def userMan(request):
#     users = User.objects.all().order_by('id')
#     people = People.objects.all().order_by('objectid')
#     userArr = []
#     peopleArr = []
#     unsyncedUsers = []
#     unsyncedPeople = []
#     for user in users:
#         userArr.append(user.id)
#     for person in people:
#         peopleArr.append(person.objectid)
#     #print peopleArr
#     #print userArr
#     for i in range(len(userArr)):
#         if userArr[i] not in peopleArr:
#             unsyncedUsers.append(users[i])
#     for i in range(len(peopleArr)):
#         if peopleArr[i] not in userArr:
#             unsyncedPeople.append(people[i])
#             #u = users[i]
#             #p = Person(objectid=u.id, firstname=u.first_name,lastname=u.last_name, email=u.email,)
#     if len(unsyncedPeople)==0:
#         unsyncedPeople = None
#     if len(unsyncedUsers)==0:
#         unsyncedUsers = None
#     #print unsyncedUsers
#     return render(request, 'lmdb/userMan.html',{'users' : unsyncedUsers, 'people' : unsyncedPeople})
# 
# @login_required(login_url='/login/')
# @permission_required('users.can_add')
# def userManForm(request):
#     if request.POST:
#         peopleForms = []
#         dict = request.POST
#         vals = dict.keys()
#         print vals
#         for val in vals:
#             if val != 'csrfmiddlewaretoken':
#                 user = User.objects.get(id=val)
#                 print user
#         return render(request, 'lmdb/userManForm.html',{'peopleForms' : peopleForms})
#     else:
#         return HttpResponseRedirect('/userMan/')

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
        org.save()
        return HttpResponse(json.dumps({'id': org.objectid, 'organismname' : org.organismname}))
    return HttpResponse('failed')

@login_required(login_url='/login/')
@user_uploaded
def editOrganism(request, org_id):
    organism = Organism.objects.get(objectid=org_id)    
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

    
#########################################################################################
#   END OF FUNCTIONS FOR ORGANISMS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR SIGHTINGS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
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

@login_required(login_url='/login/')
@user_uploaded
def sightingDetail(request, sight_id):
    sighting = get_object_or_404(Sighting, pk=sight_id)
    organism = get_object_or_404(Organism, pk=sighting.organismid.objectid)
    location = get_object_or_404(Location, pk=sighting.locationid)
    project = get_object_or_404(Project, pk=sighting.projectid.objectid)
    person =get_object_or_404(People, pk=sighting.personid.objectid)
    return render(request, 'lmdb/sightingDetail.html', {'person': person, 'project' : project,'sighting' : sighting, 'organism' : organism, 'location' : location})


@login_required(login_url='/login/')
@user_uploaded
def createSighting(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Sighting.objects.all().order_by('-objectid')[0].objectid+1
        form = SightingForm(postVals, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/data/sightings/')
    else:
        form = SightingForm(user=request.user.id)
        form.initial['objectid'] = 1
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

@login_required(login_url='/login/')
@user_uploaded
def dataUpdateSighting(request, id):
    if request.POST:
        s = Sighting.objects.get(objectid=id)
        form = SightingForm(request.POST, instance = s, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            return render(request, 'lmdb/createSighting.html', {'form' : form})
    else:
        return HttpResponse('failed')

#########################################################################################
#   END OF FUNCTIONS FOR SIGHTINGS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR CHANGES #
#########################################################################################
@login_required(login_url='/login/')
@user_uploaded
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

@login_required(login_url='/login/')
@user_uploaded
def changeDetail(request, change_id):
    change = get_object_or_404(Change, pk=change_id)
    parameter = get_object_or_404(Parameter, pk=change.parameterid.objectid)
    location = get_object_or_404(Location, pk=change.locationid)
    project = get_object_or_404(Project, pk=change.projectid.objectid)
    person =get_object_or_404(People, pk=change.personid.objectid)
    return render(request, 'lmdb/changeDetail.html', {'person': person, 'project' : project,'change' : change, 'parameter' : parameter, 'location' : location})


@login_required(login_url='/login/')
@user_uploaded
def createChange(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Change.objects.all().order_by('-objectid')[0].objectid+1
        form = ChangeForm(postVals, user=request.user.id)
        form.initial['objectid'] = Change.objects.all().order_by('-objectid')[0].objectid+1
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/data/changes/')
    else:
        form = ChangeForm(user=request.user.id)
        form.initial['objectid'] = 1
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

@login_required(login_url='/login/')
@user_uploaded
def dataUpdateChange(request, id):
    if request.POST:
        c = Change.objects.get(objectid=id)
        form = ChangeForm(request.POST, instance = c, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
           return render(request, 'lmdb/createChange.html', {'form' : form})
    else:
        return HttpResponse('failed')

#########################################################################################
#   END OF FUNCTIONS FOR CHANGES #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR MEASUREMENTS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
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


@login_required(login_url='/login/')
@user_uploaded
def measurementDetail(request, meas_id):
    measurement = get_object_or_404(Measurement, pk=meas_id)
    parameter = get_object_or_404(Parameter, pk=measurement.parameterid.objectid)
    location = get_object_or_404(Location, pk=measurement.locationid)
    project = get_object_or_404(Project, pk=measurement.projectid.objectid)
    person =get_object_or_404(People, pk=measurement.personid.objectid)
    return render(request, 'lmdb/measurementDetail.html', {'person': person, 'project' : project,'measurement' : measurement, 'parameter' : parameter, 'location' : location})

@login_required(login_url='/login/')
@user_uploaded
def createMeasurement(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Measurement.objects.all().order_by('-objectid')[0].objectid+1
        form = MeasurementForm(data=postVals, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/data/measurements/')
    else:
        form = MeasurementForm(user=request.user.id)
        form.initial['objectid'] = 1
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

@login_required(login_url='/login/')
@user_uploaded
def dataUpdateMeasurement(request, id):
    if request.POST:
        m = Measurement.objects.get(objectid=id)
        form = MeasurementForm(request.POST, instance = m, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
           return render(request, 'lmdb/createMeasurement.html', {'form' : form})
    else:
        return HttpResponse('failed')


#########################################################################################
#   END OF FUNCTIONS FOR MEASUREMENTS #
#
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR COLLECTIONS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
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


@login_required(login_url='/login/')
@user_uploaded
def collectionDetail(request, coll_id):
    collection = get_object_or_404(Collection, pk=coll_id)
    organism = get_object_or_404(Organism, pk=collection.organismid.objectid)
    location = get_object_or_404(Location, pk=collection.locationid)
    project = get_object_or_404(Project, pk=collection.projectid.objectid)
    person =get_object_or_404(People, pk=collection.personid.objectid)
    return render(request, 'lmdb/collectionDetail.html', {'person': person, 'project' : project,'collection' : collection, 'organism' : organism, 'location' : location})
    

@login_required(login_url='/login/')
@user_uploaded
def createCollection(request):
    if request.POST:
        postVals = request.POST.copy()
        postVals['objectid'] = Collection.objects.all().order_by('-objectid')[0].objectid+1
        form = CollectionForm(postVals, user=request.user.id)
        #form.fields['objectid'].initial = Collection.objects.all().order_by('-objectid')[0].objectid+1
        if form.is_valid():
            form.cleaned_data['objectid']=Collection.objects.all().order_by('-objectid')[0].objectid+1
            form.save()
            return HttpResponseRedirect('/data/collections/')
    else:
        form = CollectionForm(user=request.user.id)
        form.initial['objectid'] = 1
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

@login_required(login_url='/login/')
@user_uploaded
def dataUpdateCollection(request, id):
    if request.POST:
        c = Collection.objects.get(objectid=id)
        form = CollectionForm(request.POST, instance = c, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
           return render(request, 'lmdb/createCollection.html', {'form' : form})
    else:
        return HttpResponse('failed')


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



def login_user(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    username = password = ''
    if request.POST:
        print request.POST
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