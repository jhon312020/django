from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^authenticate/$', views.AuthenticateView.as_view()),
	url(r'^create/$', views.CreateView.as_view()),
]
