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
    
)