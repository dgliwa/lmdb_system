from django.conf.urls import patterns, url

from reporting import views

urlpatterns = patterns('',
        url(r'^$', views.reporting, name='reportingHome'),
        url(r'^testChart/$', views.reporting_test, name='reportingTest'),
        url(r'^simple/$', views.simpleReporting, name='simpleReporting'),
        url(r'^advanced/$', views.advancedReporting, name='advancedReporting'),
        url(r'^simple/csv/advanced/$', views.csvAdvancedReport, name='csvAdvancedReport'),
        url(r'^general/html/advanced/$', views.htmlAdvancedReport, name='htmlAdvancedReport'),
        url(r'^general/pdf/advanced/$', views.pdfAdvancedReport, name='pdfAdvancedReport'),
        url(r'^general/csv/simple/$', views.csvSimpleReport, name='csvSimpleReport'),
        url(r'^general/html/simple/$', views.htmlSimpleReport, name='htmlSimpleReport'),
        url(r'^general/pdf/simple/$', views.pdfSimpleReport, name='pdfSimpleReport'),



     #   url(r'^ineedhelp/', include('apps.help.urls', namespace='otherhelp', app_name='help')),

)