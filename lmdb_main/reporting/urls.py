from django.conf.urls import patterns, url

from reporting import views

urlpatterns = patterns('',
        url(r'^$', views.reporting, name='reportingHome'),
        url(r'^testChart/$', views.reporting_test, name='reportingTest'),

     #   url(r'^ineedhelp/', include('apps.help.urls', namespace='otherhelp', app_name='help')),

)