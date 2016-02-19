from django.conf.urls import url
from . import views

app_name = 'tweets'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'statuses/update/$', views.TweetView.as_view()),
	url(r'favorites/create/$', views.FavouriteView.as_view()),
]
