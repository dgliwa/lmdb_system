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
		size = len(vals.getlist('username'))
		#vals.pop('size')
		group = int(vals['group'])
		#print group
		vals.pop('group')
		if size == 1:
			form = UserCreateForm(vals)
			if form.is_valid():
					form.save()
					user = User.objects.get(username=vals['username'])
					g = Group.objects.get(id=group)
					user.groups.add(g)
					user.save()
			else:
				failed.append(form)
		else:
			for j in range(size):
				userform = {'username' : vals.getlist('username')[j], 'password1' : vals.getlist('password1')[j], 'password2' : vals.getlist('password2')[j], 'first_name':vals.getlist('first_name')[j], 'last_name' : vals.getlist('last_name')[j], 'email' : vals.getlist('email')[j]}
				print userform
				form = UserCreateForm(userform)
				print 'not 1'
				if form.is_valid():
					form.save()
					user = User.objects.get(username=userform['username'])
					g = Group.objects.get(id=group)
					print g
					user.groups.add(g)
					user.save()
				else:
					failed.append(form)
		
		if len(failed) > 0:
			return HttpResponse('some failed')

		return HttpResponseRedirect('/admin/auth/user/')
	return render(request,'customadmin/addUsers.html',{'groups' : groups})
