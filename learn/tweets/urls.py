from django.conf.urls import url
from . import views

app_name = 'tweets'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^create', views.tweet_create, name = 'tweet_create'),
	url(r'^media_create', views.tweet_media_create, name = 'tweet_media_create'),
	#url(r'^login', views.login, name = 'login'),
	#url(r'^validate', views.validate, name = 'validate'),
	url(r'^post$', views.tweet_post, name = 'tweet_post'),
	url(r'^post/media$', views.tweet_media_post, name = 'tweet_media_post')
]
