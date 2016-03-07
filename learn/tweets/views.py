from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import logging
import os
import tempfile
import json

from .models import *
# Create your views here.

logger = logging.getLogger(__name__)

# User listing view
def index(request):
	context = {'testing': 'testing'}
	return JsonResponse(context)

class MediaView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):
		if request.user is None:
			return Response(status=401)
		if request.method == 'POST':
			if self.handle_uploaded_file(request.FILES['tweet_media']):
				tweetText = request.POST['tweet_text']
				file_name = request.FILES['tweet_media']._get_name()
				tweet = TweetMedia.objects.create(user_id = request.user.id, tweet_text = tweetText, tweet_media = file_name)
				tweet.save()
				if tweet.id:
					content = {'success_message':'Successfully tweeted!'}
				else:
					content = {'error_message':'Try after some time'}
		return JsonResponse(content)

	def handle_uploaded_file(self, f):
		MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'uploads')
		file_path = os.path.join(MEDIA_ROOT, f._get_name());
		#file_path = os.path.join(MEDIA_ROOT);
		destination = open(file_path, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		return True

# Endpoint is Used for posting status update
# Returns a message
# on successful posting
# Endpoint url : /tweets/statuses/update
#{"token":"880bd799194db2f2541468af129b2499d3404147", "tweet_text":"Final testing by jr"}
class TweetView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):
		if request.user is None:
			return Response(status=401)
		params = json.loads(request.body.decode('utf-8'))
		user_status = params.get('tweet_text')
		if user_status is None or user_status == '':
			return Response(status=401)
		tweet = Tweets.objects.create(user_id = request.user.id, tweet_text = user_status)
		tweet.save()
		if tweet is None:
			return Response({'message':'Some server issue try after sometime!'})
		else:
			return Response({'message':'Status posted successfully!'})

# Endpoint is Used for posting adding favourite to a tweet
# Returns a token as a result
# on successful validation
# Endpoint url : /tweets/favorites/create
# Currently working
#{"token":"880bd799194db2f2541468af129b2499d3404147", "tweet_id":"1"}
#{"token":"de39fb3251756d3e7e75be84b3d45e9ed74e5e6e", "tweet_id":"1"}
class FavouriteView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))
		tweet_id = params.get('tweet_id')

		if request.user is None or tweet_id is None or tweet_id == '':
			return Response(status=401)
		try:
			tweet = Tweets.objects.get(id=tweet_id)
			try:
				already_voted = TweetFavourite.objects.get(user_id = request.user.id, tweet_id = tweet_id)
			except TweetFavourite.DoesNotExist:
				already_voted = None
			if request.user.id == tweet.user_id:
				return Response({'message' : 'You cannot add favourite to your own tweet!'})
			elif already_voted is None:
				tweet = TweetFavourite.objects.create(user_id = request.user.id, tweet_id = tweet_id, tweet_like = 1)
				tweet.save()
			else:
				return Response({'message':'Sorry! you have already added your vote for this tweet!'})
			if tweet is None:
				return Response({'message':'Some server issue try after sometime!'})
			else:
				return Response({'message':'Your favourite has been added!'})

		except Tweets.DoesNotExist:
			# Checking for tweet existence
			logger.info('Invalid tweet ' , tweet_id)
			return Response({'message': 'Invalid tweet id or tweet doesn\'t exsits!'})
		except Exception as exception:
			logger.error(exception)
			return Response(status=500)

# Endpoint is Used for creating friendship with user
# Returns a message
# on successful friendship creation
# Endpoint url : /tweets/friendships/create
#{"token":"880bd799194db2f2541468af129b2499d3404147", "friend_id":"2"}
class FriendCreateView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))
		
		friend_id = params.get('friend_id')
		#return Response({'message':request.user.id})
		
		if request.user is None or friend_id is None or friend_id == '':
			return Response(status=401)
		elif request.user.id == int(friend_id):
			return Response({'message':'You cannot be friend to yourself!'})
		try:
			friend_id_exists = User.objects.get(id=friend_id)
			try:
				already_is_a_friend = Friends.objects.get(user_id = request.user.id, friend_id=friend_id)
				return Response({'message': 'You have already made friendship with this person!', 'id': already_is_a_friend.friend_id})

			except Friends.DoesNotExist:
				friend = Friends.objects.create(user_id = request.user.id, friend_id = friend_id)
				friend.save()

				if friend is None:
					return Response({'message':'Some server issue try after sometime!'})
				else:
					return Response({'message':'You have currently made friendship with the user successfully!'})

		except User.DoesNotExist:
			# Returning error on unexistence of the user
			return Response({'message': 'The friendship is not possible as the user doesn\'t exists!'})

		except Exception as exception:
			logger.error(exception)
			return Response(status=500)

# Endpoint is Used get user's friend's list
# Returns a message
# on successful friendship creation
# Endpoint url : /tweets/friends/list/
#{"token":"880bd799194db2f2541468af129b2499d3404147"}
class FriendsListView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		if request.user is None:
			return Response(status=401)
		friends = Friends.objects.filter(user_id = request.user.id)
		friends_count = friends.count();
		friend_ids = []
		if friends_count > 0:
			for friend in friends:
				friend_ids.append(friend.friend_id)
			friends_list = User.objects.filter(id__in = friend_ids)
			response = map(lambda t: model_to_dict(t), friends_list)
			return Response(response)
		else:
			return Response({'message': 'Currently! no friends for the user'})
		return Response(data)

# Endpoint is Used get user's friend's list
# Returns a message
# on successful friendship creation
# Endpoint url : /tweets/followers/list
#{"token":"de39fb3251756d3e7e75be84b3d45e9ed74e5e6e"}
class FollowersListView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	#permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		if request.user is None:
			return Response(status=401)
		followers = Friends.objects.filter(friend_id = request.user.id)
		followers_count = followers.count();
		followers_ids = []
		if followers_count > 0:
			for follower in followers:
				followers_ids.append(follower.user_id)
			followers_list = User.objects.filter(id__in = followers_ids)
			response = map(lambda t: model_to_dict(t), followers_list)
			return Response(response)
		else:
			return Response({'message': 'Currently! no followers for the user'})
		return Response(data)


# Endpoint is Used get the tweets should 
# and the retweets of people the authenticated
# users follows
# Returns a list statuses/home_timeline
# on successful 
# Endpoint url : /tweets/statuses/home_timeline
#{"token":"de39fb3251756d3e7e75be84b3d45e9ed74e5e6e"}
class HomeTimeLine(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	#permission_classes = (permissions.AllowAny,)

	def get(self, request, format=None):
		if request.user is None:
			return Response(status=401)
		followers = Friends.objects.filter(user_id = request.user.id)
		followers_count = followers.count();
		followers_ids = []
		# Adding the authenticated user id
		followers_ids.append(request.user.id)
		if followers_count > 0:
			for follower in followers:
				followers_ids.append(follower.friend_id)
			#print followers_ids
			tweet_list = Tweets.objects.filter(user_id__in = followers_ids)
			response = map(lambda t: model_to_dict(t), tweet_list)
			return Response(response)
		else:
			return Response({'message': 'Currently no tweets'})
		return Response(data)
