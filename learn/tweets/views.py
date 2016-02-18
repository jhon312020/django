from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

import os
import tempfile

from .models import Tweets, Tweet_media
# Create your views here.

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

# User tweet posting
def tweet_media_create(request):
	userName = 'cygnusbala'
	user = User.objects.get(username=userName)
	token = Token.objects.get(user=user)
	content = {'token': token.key}
	return render(request, 'tweets/tweet_media.html', content)

def tweet_post(request):
	if request.method == 'POST':
		token = request.POST['token']
		token = Token.objects.get(key=token)
		if token is not None:
			# Getting the stored rest framework token
			tweetText = request.POST['tweet_text']
			tweet = Tweets.objects.create(user_id = token.user_id, tweet_text = tweetText)
			tweet.save()
			if tweet.id:
				content = {'success_message':'Successfully tweeted!'}
			else:
				content = {'error_message':'Try after some time'}
	return JsonResponse(content)

def tweet_media_post(request):
	if request.method == 'POST':
		token = request.POST['token']
		token = Token.objects.get(key=token)
		if token is not None:
			# Getting the stored rest framework token
			tweetText = request.POST['tweet_text']
			if handle_uploaded_file(request.FILES['tweet_media']):
				file_name = request.FILES['tweet_media']._get_name()
				tweet = Tweet_media.objects.create(user_id = token.user_id, tweet_text = tweetText, tweet_media = file_name)
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

