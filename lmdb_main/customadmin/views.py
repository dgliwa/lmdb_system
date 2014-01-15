# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from lmdb.decorators import user_uploaded
from django.http import *
from django.contrib.auth.models import User, Permission


 

@user_uploaded
@login_required(login_url='/lmdb/login/')
def addUsers(request):
	perms = Permission.objects.all()
	return render(request,'customadmin/addUsers.html',{'perms' : perms})
