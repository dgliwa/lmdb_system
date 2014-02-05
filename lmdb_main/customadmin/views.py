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
		size = int(request.POST['size'])
		for i in range(0,size):
			vals = json.loads(json.dumps(request.POST))
			print vals
			form = UserCreateForm()
			x = int(vals['size'])
			vals.pop('size')
			if x == 1:
				form = UserCreateForm(vals)
				print '1'
				#form = UserCreationForm(username=request.POST['username'], password1 = request.POST['password1'], password2 = request.POST['password2'])
			    # form.initial['username'] = vals['username']
			    # form.initial['password1'] = vals['password1']
			    # form.initial['password2'] = vals['password2']
			else:
				for i in range(x):
				    userform = {'username' : vals['username'][i], 'password1' : vals['password1'][i], 'password2' : vals['password2'][i], 'first_name':vals['first_name'][i], 'last_name' : vals['last_name'][i], 'email' : vals['email'][i]}
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
