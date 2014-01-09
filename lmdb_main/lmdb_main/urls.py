from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lmdb_main.views.home', name='home'),
    # url(r'^lmdb_main/', include('testlurec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^lmdb/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^lmdb/admin/', include(admin.site.urls)),
     url(r'^lmdb/', include('lmdb.urls', namespace='lmdb')),
     url(r'^lmdb/login/$', 'lmdb.views.login_user'),
     
)