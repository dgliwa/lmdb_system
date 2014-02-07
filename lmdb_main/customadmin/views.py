# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from lmdb.decorators import user_uploaded
from django.http import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from customadmin.forms import *
import json



 

@user_uploaded
@login_required(login_url='/lmdb/login/')
def addUsers(request):
	groups = Group.objects.all()
	if request.POST:
		failed = []
		vals = request.POST.copy()
		size = int(vals['size'])
		print request.POST['username']
		print vals['username']
		print vals
		for i in range(0,size):
			print vals
			form = UserCreateForm()
			x = int(vals['size'])
			vals.pop('size')
			if x == 1:
				form = UserCreateForm(vals)
				print '1'
				#form = UserCreationForm(username=request.POST['username'], password1 = request.POST['password1'], password2 = request.POST['password2'])
			    # form.initial['username'] = request.POST['username']
			    # form.initial['password1'] = request.POST['password1']
			    # form.initial['password2'] = request.POST['password2']
			else:
				for j in range(x):
					print j
					userform = {'username' : vals.getlist('username')[j], 'password1' : vals.getlist('password1')[j], 'password2' : vals.getlist('password2')[j], 'first_name':vals.getlist('first_name')[j], 'last_name' : vals.getlist('last_name')[j], 'email' : vals.getlist('email')[j]}
					form = UserCreateForm(userform)
					print 'not 1'
			#print form.initial['password1']
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/admin/auth/user/')
			else:
				print 'fail'
				#print form.errors
		return render(request,'customadmin/addUsers.html',{'groups' : groups})
	return render(request,'customadmin/addUsers.html',{'groups' : groups})
