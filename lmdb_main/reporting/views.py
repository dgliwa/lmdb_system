# Create your views here.
from lmdb.decorators import user_uploaded 
from django.contrib.auth.decorators import login_required

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
from django.utils.safestring import mark_safe


from lmdb.decorators import user_uploaded 
import json
import datetime
import calendar
import csv


@login_required(login_url='/login/')
@user_uploaded
def reporting(request):
    
    return render(request,'reporting/reporting.html',{})

@login_required(login_url='/login/')
@user_uploaded
def reporting_test(request):
	date = datetime.datetime.now()
	year = date.year
	month = date.month
	xaxis = []
	sightings = []
	collections = []
	changes = []
	measurements = []
	for i in range(12):
		day = calendar.monthrange(year,month)[1]
		xaxis.append(calendar.month_name[month] + " " + str(year))
		a = Sighting.objects.filter(date__range=[str(year)+"-"+str(month)+"-01", str(year)+"-"+str(month)+"-"+str(day)]).count()
		b = Collection.objects.filter(datecollect__range=[str(year)+"-"+str(month)+"-01", str(year)+"-"+str(month)+"-"+str(day)]).count()
		c = Change.objects.filter(date__range=[str(year)+"-"+str(month)+"-01", str(year)+"-"+str(month)+"-"+str(day)]).count()
		d = Measurement.objects.filter(date__range=[str(year)+"-"+str(month)+"-01", str(year)+"-"+str(month)+"-"+str(day)]).count()
		sightings.append(a)
		collections.append(b)
		changes.append(c)
		measurements.append(d)
		if month == 1:
			month = 12
			year = year - 1
		else:
			month = month-1
	xaxis.reverse()
	sightings.reverse()
	collections.reverse()
	changes.reverse()
	measurements.reverse()
	xaxis = mark_safe(xaxis)
	return render(request, 'reporting/reportingTest.html',{'collections':collections, 'sightings':sightings, 'changes':changes, 'measurements':measurements, 'xaxis' : xaxis})


@login_required(login_url='/login/')
@user_uploaded
def generalReporting(request):
	sightings = Sighting.objects.all()
	measurements = Measurement.objects.all()
	collections = Collection.objects.all()
	changes = Change.objects.all()
	return render(request,'reporting/generalReporting.html',{'sightings':sightings,'measurements':measurements,'collections':collections,'changes':changes})



@login_required(login_url='/login/')
@user_uploaded
def csvReport(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="general_report.csv"'
	writer = csv.writer(response)
	print request
	if request.POST:
		dict = request.POST
		vals = dict.keys()
		changes = []
		collections = []
		measurements = []
		sightings = []
		for val in vals:
			if val != 'csrfmiddlewaretoken':
				split = dict[val].split(',')
				if split[0] == 'Change':
					changes.append(split[1])
				elif split[0] == 'Sighting':
					sightings.append(split[1])
				elif split[0] == 'Measurement':
					measurements.append(split[1])
				elif split[0] == 'Collection':
					collections.append(split[1])
		if len(changes) != 0:
			writer.writerow(['Changes'])
			writer.writerow(['Change ID','Project Name','Project Start Date','Project End Date','Project Description', 'Project Location ID', 'Project Owner','Change Description','Change Justification','Parameter Name','Change Date','Person','Change Location ID'])
			for c1 in changes:
				c = Change.objects.get(objectid=int(c1))
				writer.writerow([c.objectid, c.projectid.projectname, c.projectid.projectstartdate, c.projectid.projectenddate, c.projectid.projectdescription, c.projectid.locationid, c.projectid.personid.displayname, c.description, c.justification, c.parameterid.commonname, c.date, c.personid.displayname, c.locationid, ])
				writer.writerow([])
		if len(collections) != 0:
			writer.writerow(['Collections'])
			writer.writerow(['Collection ID','Project Name','Project Start Date','Project End Date','Project Description', 'Project Location ID', 'Project Owner','Collection Method','Organism Name','Collection Date','Person','Collection Location ID'])
			for c1 in collections:
				c = Collection.objects.get(objectid=int(c1))
				print c.objectid
				writer.writerow([c.objectid, c.projectid.projectname, c.projectid.projectstartdate, c.projectid.projectenddate, c.projectid.projectdescription, c.projectid.locationid, c.projectid.personid.displayname, c.methodcollect, c.organismid.organismname, c.datecollect, c.personid.displayname, c.locationid, ])
				writer.writerow([])
		if len(measurements) != 0:
			writer.writerow(['Measurements'])
			writer.writerow(['Measurement ID','Project Name','Project Start Date','Project End Date','Project Description', 'Project Location ID', 'Project Owner','Measurement Name','Measurement Method','Measurement Quantity','Measurement Units','Measurement Notes','Measurement Medium','Parameter Name','Measurement Date','Person','Measurement Location ID'])
			for m1 in measurements:
				m = Measurement.objects.get(objectid=int(m1))
				writer.writerow([m.objectid, m.projectid.projectname, m.projectid.projectstartdate, m.projectid.projectenddate, m.projectid.projectdescription, m.projectid.locationid, m.projectid.personid.displayname, m.mname, m.mmethod, m.mquant, m.munits, m.notes, m.medium, m.parameterid.commonname, m.date, m.personid.displayname, m.locationid, ])
				writer.writerow([])
		if len(sightings) != 0:
			writer.writerow(['Sightings'])
			writer.writerow(['Sighting ID','Project Name','Project Start Date','Project End Date','Project Description', 'Project Location ID', 'Project Owner','Organism Name','Number Sighted','Sighting Date','Sighting Notes','Person','Sighting Location ID'])
			for s1 in sightings:
				s = Sighting.objects.get(objectid=int(s1))
				writer.writerow([s.objectid, s.projectid.projectname, s.projectid.projectstartdate, s.projectid.projectenddate, s.projectid.projectdescription, s.projectid.locationid, s.projectid.personid.displayname, s.organismid.organismname, s.number, s.date, s.notes, s.personid.displayname, s.locationid, ])
				writer.writerow([])

	return response
	#return HttpResponse('ok')


