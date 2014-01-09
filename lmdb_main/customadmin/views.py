# Create your views here.


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from lmdb.decorators import user_uploaded
from django.http import *
 

@user_uploaded
@login_required(login_url='/lmdb/login/')
def addUsers(request):
	return HttpResponse('ok')