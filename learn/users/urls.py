from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^register$', views.register, name = 'register'),
	url(r'^login', views.login, name = 'login'),
	url(r'^validate', views.validate, name = 'validate'),
	url(r'^user_create$', views.user_create, name = 'user_create')
]
