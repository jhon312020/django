from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^list/$', views.list, name='list'),
	url(r'^create/$', views.user_create, name='user_create'),
	url(r'^authenticate/$', views.login, name='login'),
]