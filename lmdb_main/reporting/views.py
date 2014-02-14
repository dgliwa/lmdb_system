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


@login_required(login_url='/login/')
@user_uploaded
def reporting(request):
    
    return render(request,'reporting/reporting.html',{})