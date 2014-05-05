from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from customadmin.views import addUsers
from proxy.views import proxy_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lmdb_main.views.home', name='home'),
    # url(r'^lmdb_main/', include('testlurec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/auth/user/add/test', addUsers),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^', include('lmdb.urls', namespace='lmdb')),
     url(r'^accounts/login/$', 'lmdb.views.login_user'),
     url(r'^login/$', 'lmdb.views.login_user'),
     url(r'^proxy/(?P<path>.*)$', proxy_to),
     url(r'^data/', include('data.urls', namespace='data')),
     url(r'^reporting/', include('reporting.urls', namespace='reporting')),
     url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/password/reset/done/'}),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/password/done/'}),
    url(r'^password/done/$', 'lmdb.views.done'),

)
