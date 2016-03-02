from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

import json
import logging
from .models import *

def make_user(username, password):
	user = User.objects.create_user(username, None, password)
	user.save()
	token = Token.objects.create(user=user)
	return token

def make_tweet(user_id, user_status):
	tweet = Tweets.objects.create(user_id = user_id, tweet_text = user_status)
	tweet.save()
	return tweet


# Create your tests here.


# Create your tests here.
# Test cases to test success
# and failure conditions
# on Tweet posting

class TweetTests(APITestCase):
	def test_authenticate_successfully(self):
		user = make_user('jr', 'password')
		
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/statuses/update', {'tweet_text':'Posted by JR'}, format='json')
		self.assertEqual(response.status_code, 200)

		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'Status posted successfully!')

	def test_token_validity(self):
		user = make_user('jr', 'password')
		
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'duwuwuuwuwu')
		response = self.client.post('/tweets/statuses/update', {'tweet_text':'Posted by JR'}, format='json')
		self.assertEqual(response.status_code, 401)
	
	def test_empty_fields(self):
		user = make_user('jr', 'password')
		
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/statuses/update', {'tweet_text':''}, format='json')
		self.assertEqual(response.status_code, 401)
	
	def test_missing_fields(self):
		user = make_user('jr', 'password')
		
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/statuses/update', {}, format='json')
		self.assertEqual(response.status_code, 401)

# Create your tests here.
# Test cases to test success
# and failure conditions
# on Tweet Favourite

class FavouriteTests(APITestCase):
	def test_favourite_successfully(self):
		user = make_user('jr', 'password')
		tweet = make_tweet(user.user_id, 'created by JR')
		#self.assertEqual(response.status_code, 200)

		user = make_user('jr2', 'password')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/favorites/create', {'tweet_id':tweet.id}, format='json')
		self.assertEqual(response.status_code, 200)
		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'Your favourite has been added!')

	def test_favourite_for_own_tweet(self):
		user = make_user('jr', 'password')
		tweet = make_tweet(user.user_id, 'created by JR')

		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/favorites/create', {'tweet_id':tweet.id}, format='json')
		self.assertEqual(response.status_code, 200)
		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'You cannot add favourite to your own tweet!')

	def test_already_added_favourite(self):
		user = make_user('jr', 'password')
		tweet = make_tweet(user.user_id, 'created by JR')
		user = make_user('jr2', 'password')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/favorites/create', {'tweet_id':tweet.id}, format='json')
		self.assertEqual(response.status_code, 200)
		response = self.client.post('/tweets/favorites/create', {'tweet_id':tweet.id}, format='json')
		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'Sorry! you have already added your vote for this tweet!')
	 
	def test_missing_fields(self):
		user = make_user('jr', 'password')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.key)
		response = self.client.post('/tweets/favorites/create', {'tweet_id':tweet.id}, format='json')
		self.assertEqual(response.status_code, 200)
		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'Invalid tweet id or tweet doesn\'t exsits!')
