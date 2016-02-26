from django.conf.urls import url
from . import views

app_name = 'tweets'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'statuses/update$', views.TweetView.as_view()),
	url(r'favorites/create$', views.FavouriteView.as_view()),
	url(r'friendships/create$', views.FriendCreateView.as_view()),
	url(r'friends/list$', views.FriendsListView.as_view()),
	url(r'followers/list$', views.FollowersListView.as_view()),
	url(r'media/upload$', views.MediaView.as_view()),
]


