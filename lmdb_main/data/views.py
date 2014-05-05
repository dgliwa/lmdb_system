from lmdb.decorators import user_uploaded 

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

from lmdb.forms import *
import json


@login_required(login_url='/login/')
@user_uploaded
def data(request):
    return render(request,'data/data.html',{})


# Create your views here.
#########################################################################################
#   BEGINNING OF FUNCTIONS FOR SIGHTINGS #
#########################################################################################

@login_required(login_url='/login/')
@user_uploaded
def sightings(request):    # !!!!!!   NEED TO APPLY FKEY RESTRAINTS
    sightings = Sighting.objects.all()
    print sightings
    points = []
    lines = []
    polys = []
    for s in sightings:
        location = Location.objects.get(pk = s.locationid)
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)


    template = loader.get_template('data/sightings.html')
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
    return render(request, 'data/sightingDetail.html', {'person': person, 'project' : project,'sighting' : sighting, 'organism' : organism, 'location' : location})


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

    return render(request, 'data/createSighting.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})

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
            return render(request, 'data/createSighting.html', {'form' : form})
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
    changes = Change.objects.all()
    points = []
    lines = []
    polys = []
    for c in changes:
        location = Location.objects.get(pk = c.locationid)
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)

    template = loader.get_template('data/changes.html')
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
    return render(request, 'data/changeDetail.html', {'person': person, 'project' : project,'change' : change, 'parameter' : parameter, 'location' : location})


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

    return render(request, 'data/createChange.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})

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
           return render(request, 'data/createChange.html', {'form' : form})
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
    measurements = Measurement.objects.all()
    points = []
    lines = []
    polys = []
    for m in measurements:
        location = Location.objects.get(pk = m.locationid)
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)
    template = loader.get_template('data/measurements.html')
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
    return render(request, 'data/measurementDetail.html', {'person': person, 'project' : project,'measurement' : measurement, 'parameter' : parameter, 'location' : location})

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

    return render(request, 'data/createMeasurement.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})

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
           return render(request, 'data/createMeasurement.html', {'form' : form})
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
def collections(request):    
    collections = Collection.objects.all()
    points = []
    lines = []
    polys = []
    for c in collections:
        location = Location.objects.get(pk = c.locationid)
        if location.pointid != None:
            points.append(location.pointid)
        elif location.lineid != None:
            lines.append(location.lineid)
        elif location.areaid != None:
            polys.append(location.areaid)


    template = loader.get_template('data/collections.html')
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
    return render(request, 'data/collectionDetail.html', {'person': person, 'project' : project,'collection' : collection, 'organism' : organism, 'location' : location})
    

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

    return render(request, 'data/createCollection.html', {'form' : form, 'points':points, 'lines':lines,'polys':polys})

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
           return render(request, 'data/createCollection.html', {'form' : form})
    else:
        return HttpResponse('failed')


#########################################################################################
#   END OF FUNCTIONS FOR COLLECTIONS #
#
#########################################################################################

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
    return render(request,'data/dataUpdate.html',{'sightings':sightings,'measurements':measurements,'collections':collections,'changes':changes})

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
        
    return render(request,'data/dataUpdateForm.html',{'collectionforms':collectionforms, 'changeforms':changeforms,'measurementforms':measurementforms,'sightingforms':sightingforms, 'points':points, 'lines':lines,'polys':polys})
