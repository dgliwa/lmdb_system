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
from lmdb.decorators import user_uploaded 
import json
import datetime
import calendar
from django.utils.safestring import mark_safe


@login_required(login_url='/login/')
@user_uploaded
def reporting(request):
    
    return render(request,'reporting/reporting.html',{})


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