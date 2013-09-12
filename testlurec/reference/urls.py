from django.conf.urls import patterns, url

from reference import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^events/$', views.events, name='events'),
    url(r'^events/(?P<event_id>\d+)/$', views.eventDetail, name='eventDetail'),
    url(r'^events/create/$', views.createEvent, name='createEvent'),
    url(r'^parameters/$', views.parameters, name='parameters'),
    url(r'^parameters/(?P<param_id>\d+)/$', views.paramDetail, name='paramDetail'),
    url(r'^parameters/create/$', views.createParam, name='createParam'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<project_id>\d+)/$', views.projectDetail, name='projectDetail'),
    url(r'^projects/create/$', views.createProject, name='createProject'),
    url(r'^permits/$', views.permits, name='permits'),
    url(r'^permits/(?P<permit_id>\d+)/$', views.permitDetail, name='permitDetail'),
    url(r'^permits/create/$', views.createPermit, name='createPermit'),
    
)