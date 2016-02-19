from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response

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

# User tweet posting
def tweet_create(request):
	userName = 'cygnusbala'
	user = User.objects.get(username=userName)
	token = Token.objects.get(user=user)
	content = {'token': token.key}
	return render(request, 'tweets/tweet.html', content)

def tweet_media_post(request):
	if request.method == 'POST':
		token = request.POST['token']
		token = Token.objects.get(key=token)
		if token is not None:
			# Getting the stored rest framework token
			tweetText = request.POST['tweet_text']
			if handle_uploaded_file(request.FILES['tweet_media']):
				file_name = request.FILES['tweet_media']._get_name()
				tweet = TweetMedia.objects.create(user_id = token.user_id, tweet_text = tweetText, tweet_media = file_name)
				tweet.save()
				if tweet.id:
					content = {'success_message':'Successfully tweeted!'}
				else:
					content = {'error_message':'Try after some time'}
	return JsonResponse(content)

def handle_uploaded_file(f):
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
# Endpoint url : /tweets/statuses/update/
class TweetView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	#permission_classes = (permissions.AllowAny,)
	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))

		token_value = params.get('token')

		if token_value is None:
			return Response(status=401)
		try:
			token = Token.objects.get(key=token_value)
			user_status = params.get('tweet_text')
			#{"token":"880bd799194db2f2541468af129b2499d3404147", "tweet_text":"Final testing by jr"}
			tweet = Tweets.objects.create(user_id = token.user_id, tweet_text = user_status)
			tweet.save()
			if tweet is None:
				return Response({'message':'Some server issue try after sometime!'})
			else:
				return Response({'message':'Status posted successfully!'})
		except token.DoesNotExist:
			# For security purposes, the user not existing returns
			# the same code as invalid credentails
			logger.info('Invalid token ' + token_value)
			return Response({'message': 'Invalid token, Kindly login again'})
		except Exception as exception:
			logger.error(exception)
			return Response(status=500)

# Endpoint is Used for posting adding favourite to a tweet
# Returns a token as a result
# on successful validation
# Endpoint url : /tweets/favorites/create/
# Currently working

class FavouriteView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	#permission_classes = (permissions.AllowAny,)
	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))

		token_value = params.get('token')
		tweet_id = params.get('tweet_id')

		if token_value is None or tweet_id is None:
			return Response(status=401)
		try:
			token = Token.objects.get(key=token_value)
			tweet = Tweets.objects.get(id=tweet_id)
			#{"token":"880bd799194db2f2541468af129b2499d3404147", "tweet_id":"1"}
			tweet = TweetFavourite.objects.create(user_id = token.user_id, tweet_id = tweet_id, tweet_like = 1)
			tweet.save()
			if tweet is None:
				return Response({'message':'Some server issue try after sometime!'})
			else:
				return Response({'message':'Your favourite has been added!'})
		except token.DoesNotExist or tweet.DoesNotExist:
			# Checking for token existence
			logger.info('Invalid token ' + token_value)
			return Response({'message': 'Invalid token, Kindly login again'})
		except tweet.DoesNotExist:
			# Checking for tweet existence
			logger.info('Invalid tweet ' + tweet_id)
			return Response({'message': 'Invalid token, Kindly login again'})
		except Exception as exception:
			logger.error(exception)
			return Response(status=500)
