from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^list/$', views.list, name='list'),
	url(r'^create/$', views.user_register, name='user_register'),
	url(r'^validate/$', views.user_create, name='validate'),
	url(r'^authenticate/$', views.login, name='login'),
]
