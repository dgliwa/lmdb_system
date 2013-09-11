from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


###logout(request) 

#handles the logins of users and holds home page

@login_required(login_url='/login/')
def index(request):
    return render(request,'home/index.html',{})


def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/home/')
    return render_to_response('login.html', context_instance=RequestContext(request))
    
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/home/login')