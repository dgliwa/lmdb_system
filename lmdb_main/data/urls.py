from django.conf.urls import patterns, url

from data import views

urlpatterns = patterns('',
    url(r'^$', views.data, name='data'),
    url(r'^update/$', views.dataUpdate, name='dataUpdate'),
    url(r'^delete/$', views.dataDelete, name='dataDelete'),
    url(r'^update/form/$', views.dataUpdateForm, name='dataUpdateForm'),
    url(r'^update/form/measurement/(?P<id>\d+)/$', views.dataUpdateMeasurement, name='dataUpdateMeasurement'),        
    url(r'^update/form/collection/(?P<id>\d+)/$', views.dataUpdateCollection, name='dataUpdateCollection'),
    url(r'^update/form/change/(?P<id>\d+)/$', views.dataUpdateChange, name='dataUpdateChange'),
    url(r'^update/form/sighting/(?P<id>\d+)/$', views.dataUpdateSighting, name='dataUpdateSighting'),
    url(r'^sightings/$', views.sightings, name='sightings'),
    url(r'^sightings/(?P<sight_id>\d+)/$', views.sightingDetail, name='sightingDetail'),
    url(r'^sightings/create/$', views.createSighting, name='createSighting'),
    url(r'^measurements/$', views.measurements, name='measurements'),
    url(r'^measurements/(?P<meas_id>\d+)/$', views.measurementDetail, name='measurementDetail'),
    url(r'^measurements/create/$', views.createMeasurement, name='createMeasurement'),
    url(r'^changes/$', views.changes, name='changes'),
    url(r'^changes/(?P<change_id>\d+)/$', views.changeDetail, name='changeDetail'),
    url(r'^changes/create/$', views.createChange, name='createChange'),
    url(r'^collections/$', views.collections, name='collections'),
    url(r'^collections/(?P<coll_id>\d+)/$', views.collectionDetail, name='collectionDetail'),
    url(r'^collections/create/$', views.createCollection, name='createCollection'),
    )