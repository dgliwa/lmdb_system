# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from lmdb.decorators import user_uploaded
from django.http import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


 

@user_uploaded
@login_required(login_url='/lmdb/login/')
def addUsers(request):
	groups = Group.objects.all()
	if request.POST:
		failed = []
		size = int(request.POST['size'])
		for i in range(0,size):
			form = UserCreationForm()
			form.initial['username'] = request.POST['username'][i]
			form.initial['password1'] = request.POST['password1'][i]
			form.initial['password2'] = request.POST['password2'][i]
			print form
			if form.is_valid():
				form.save()
				return HttpRequestRedirect('/admin/auth/user/')
			else:
				print form.errors
		return render(request,'customadmin/addUsers.html',{'groups' : groups})
	return render(request,'customadmin/addUsers.html',{'groups' : groups})
