from django.conf.urls import patterns, url

from lmdb import views

urlpatterns = patterns('',
    url(r'^logout/$', views.userlogout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^updateUser/$', views.updateUser, name='updateUser'),
    url(r'^updateUser/passwordreset/$', views.passwordreset, name='passwordreset'),
#    url(r'^userMan/form/$', views.userManForm, name='userManForm'),
    url(r'^reference/$', views.reference, name='reference'),
    url(r'^reference/events/$', views.events, name='events'),
    url(r'^reference/events/(?P<event_id>\d+)/$', views.eventDetail, name='eventDetail'),
    url(r'^reference/events/(?P<event_id>\d+)/edit/$', views.editEvent, name='editEvent'),
    url(r'^reference/events/create/$', views.createEvent, name='createEvent'),
    url(r'^reference/parameters/$', views.parameters, name='parameters'),
    url(r'^reference/parameters/(?P<param_id>\d+)/$', views.paramDetail, name='paramDetail'),
    url(r'^reference/parameters/(?P<param_id>\d+)/edit/$', views.editParam, name='editParam'),
    url(r'^reference/parameters/create/$', views.createParam, name='createParam'),
    url(r'^reference/parameters/createFromData/$', views.createParamFromData, name='createParamFromData'),
    url(r'^reference/projects/$', views.projects, name='projects'),
    url(r'^reference/projects/(?P<project_id>\d+)/$', views.projectDetail, name='projectDetail'),
    url(r'^reference/projects/(?P<project_id>\d+)/edit/$', views.editProject, name='editProject'),
    url(r'^reference/projects/(?P<project_id>\d+)/edit/addPeople/$', views.addProjectPeople, name='addProjectPeople'),
    url(r'^reference/projects/(?P<project_id>\d+)/edit/removePeople/$', views.removeProjectPeople, name='removeProjectPeople'),
    url(r'^reference/projects/create/$', views.createProject, name='createProject'),
    url(r'^reference/permits/$', views.permits, name='permits'),
    url(r'^reference/permits/(?P<permit_id>\d+)/$', views.permitDetail, name='permitDetail'),
    url(r'^reference/permits/(?P<permit_id>\d+)/edit/$', views.editPermit, name='editPermit'),
    url(r'^reference/permits/create/$', views.createPermit, name='createPermit'),
    url(r'^reference/locations/$', views.locations, name='locations'),
    url(r'^reference/locations/cleanup/$', views.locationCleanup, name='locationCleanup'),
    url(r'^reference/locations/(?P<location_id>\d+)/$', views.locationDetail, name='locationDetail'),
    url(r'^reference/locations/(?P<location_id>\d+)/edit/$', views.editLocation, name='editLocation'),
    url(r'^reference/locations/create/map/$', views.createLocationMap, name='createLocationMap'),
    url(r'^reference/locations/create/$', views.createLocation, name='createLocation'),
    url(r'^reference/locations/create/popup/$', views.createLocationPopUp, name='createLocationPopUp'),    
    url(r'^reference/organisms/$', views.organisms, name='organisms'),
    url(r'^reference/organisms/(?P<org_id>\d+)/$', views.organismDetail, name='organismDetail'),
    url(r'^reference/organisms/(?P<org_id>\d+)/edit/$', views.editOrganism, name='editOrganism'),
    url(r'^reference/organisms/create/$', views.createOrganism, name='createOrganism'),
    url(r'^reference/organisms/createFromData/$', views.createOrganismFromData, name='createOrganismFromData'),
    url(r'^reference/organisms/kingdomFilter/(?P<king_id>\w+)/$', views.kingdomFilter, name='kingdomFilter'),
    url(r'^reference/organisms/phylumFilter/(?P<phyl_id>[\w|\W]+)/$', views.phylumFilter, name='phylumFilter'),
    url(r'^reference/organisms/classFilter/(?P<class_id>[\w|\W]+)/$', views.classFilter, name='classFilter'),
    url(r'^reference/organisms/plant/classFilter/(?P<class_id>[\w|\W]+)/$', views.plantClassFilter, name='plantClassFilter'),
    url(r'^reference/organisms/orderFilter/(?P<order_id>[\w|\W]+)/$', views.orderFilter, name='orderFilter'),
    url(r'^reference/organisms/familyFilter/(?P<family_id>[\w|\W]+)/$', views.familyFilter, name='familyFilter'),
    url(r'^reference/organisms/genusFilter/(?P<genus_id>[\w|\W]+)/$', views.genusFilter, name='genusFilter'),
    url(r'^reference/organisms/(?P<column>\w+)/(?P<filter>[\w|\W]+)/$', views.species, name='species'),
    
    #url(r'^reporting/$', views.reporting, name='reporting'),

)