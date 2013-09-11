from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.userlogout, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
    'template_name': 'login.html'
}),

)