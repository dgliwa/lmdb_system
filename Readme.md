# Welcome to the LUREC LMDB System Repository

Introduction to the System
--------------------------
The purpose of the LMDB System is to provide an application where users can submit data recorded on LUREC's grounds.  This data falls in to four categories:

* Changes
* Collections
* Measurements
* Sightings

The inputted data provides information on known **parameters** and **organisms** on the LUREC grounds.  The recordings on plotted on a map of LUREC using a spatial database.

Tools
-----------------

The **LMDB System** was developed using two main tools:

* [Django](https://www.djangoproject.com/)
* [ArcGIS](https://developers.arcgis.com/javascript/)

Great tutorials can be found on those websites to supplement the information on this Readme.

Code
------------------
There are three main sections of the code:

* The LMDB (reference) section
* The data input section
* The reporting section

These sections are writted as separate django 'apps', and are in their own directory of the system.

The directory that ties these 'apps' together is the **lmdb_main** directory. In here you will find the settings.py directory, which has the settings for static files, the databases, and the installed django apps.

---
Django is a Model View Controller (or as some would call it, Model View Template) framework.  It is implemented by a url router directing an http request to what django calls views, which then render templates to be sent back as a response.

The lmdb_main urls.py router handles the major routing, and sends specific requests to the django app urls.py files.

```
urlpatterns = patterns('',
	...
     url(r'^', include('lmdb.urls', namespace='lmdb')),
     url(r'^data/', include('data.urls', namespace='data')),
     url(r'^reporting/', include('reporting.urls', namespace='reporting')),
     ...
)
```
As you can see, specific urls such as those starting with 'data/' or 'reporting/' are routed to the reporting and data apps.

---
Each app has its own views.py file.  The functions in the views.py file do various activities, such as save, update, delete, or get models, and render them in a template before sending a response.
Here is an example views function:

```
@login_required(login_url='/login/')
@user_uploaded
def organisms(request):
    organisms = Organism.objects.all().order_by('organismname')
    template = loader.get_template('lmdb/organisms.html')
    context = RequestContext( request, {
        'organisms' : organisms,
    })
    return HttpResponse(template.render(context))
 ```
 