from django.conf.urls import patterns, url

from lmdb import views

urlpatterns = patterns('',
    url(r'^logout/$', views.userlogout, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
    'template_name': 'login.html'
}),
    url(r'^$', views.index, name='index'),
    url(r'^reference/$', views.reference, name='reference'),
    url(r'^reference/events/$', views.events, name='events'),
    url(r'^reference/events/(?P<event_id>\d+)/$', views.eventDetail, name='eventDetail'),
    url(r'^reference/events/create/$', views.createEvent, name='createEvent'),
    url(r'^reference/parameters/$', views.parameters, name='parameters'),
    url(r'^reference/parameters/(?P<param_id>\d+)/$', views.paramDetail, name='paramDetail'),
    url(r'^reference/parameters/create/$', views.createParam, name='createParam'),
    url(r'^reference/projects/$', views.projects, name='projects'),
    url(r'^reference/projects/(?P<project_id>\d+)/$', views.projectDetail, name='projectDetail'),
    url(r'^reference/projects/create/$', views.createProject, name='createProject'),
    url(r'^reference/permits/$', views.permits, name='permits'),
    url(r'^reference/permits/(?P<permit_id>\d+)/$', views.permitDetail, name='permitDetail'),
    url(r'^reference/permits/create/$', views.createPermit, name='createPermit'),
    url(r'^reference/locations/$', views.locations, name='locations'),
    url(r'^reference/locations/(?P<location_id>\d+)/$', views.locationDetail, name='locationDetail'),
    url(r'^reference/locations/create/map/$', views.createLocationMap, name='createLocationMap'),
    url(r'^reference/locations/create/$', views.createLocation, name='createLocation'),
    url(r'^reference/organisms/$', views.organisms, name='organisms'),
    url(r'^reference/organisms/(?P<org_id>\d+)/$', views.organismDetail, name='organismDetail'),
    url(r'^reference/organisms/create/$', views.createOrganism, name='createOrganism'),
    url(r'^reference/organisms/kingdomFilter/(?P<king_id>\w+)/$', views.kingdomFilter, name='kingdomFilter'),
    url(r'^reference/organisms/phylumFilter/(?P<phyl_id>\w+)/$', views.phylumFilter, name='phylumFilter'),
    url(r'^reference/organisms/classFilter/(?P<class_id>\w+)/$', views.classFilter, name='classFilter'),
    url(r'^reference/organisms/orderFilter/(?P<order_id>\w+)/$', views.orderFilter, name='orderFilter'),
    url(r'^reference/organisms/familyFilter/(?P<family_id>\w+)/$', views.familyFilter, name='familyFilter'),






)