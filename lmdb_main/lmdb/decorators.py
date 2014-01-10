from lmdb.models import People
from django.contrib.auth.models import User
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import available_attrs

#no parameter
def user_uploaded(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        if People.objects.filter(objectid=request.user.id).count() != 0:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/updateUser/')
    return wrapper