from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

import json

def make_user(username, password):
	user = User.objects.create_user(username, None, password)
	user.save()
	token = Token.objects.create(user=user)
	return token

# Create your tests here.
# Test cases to test success
# and failure conditions
# on authentication

class AuthenticateTests(APITestCase):
	def test_authenticate_successfully(self):
		user = make_user('jr', 'password')
		response = self.client.post('/users/authenticate/', {'username':'jr', 'password':'password'}, format='json')
		self.assertEqual(response.status_code, 200)

		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['token'], Token.objects.get(user=user.user).key)

	def test_invalid_credentials(self):
		response = self.client.post('/users/authenticate/', {'username':'dss', 'password':'sds'}, format='json')
		#self.assertEqual(response.status_code, 401)
		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['message'], 'Invalid username/password or account doesn\'t exists')

	def test_missing_fields(self):
		response = self.client.post('/users/authenticate/', {}, format='json')
		self.assertEqual(response.status_code, 401)

# Test cases to test success
# and failure conditions
# on Creation

class CreateTests(APITestCase):

	def test_register_successfully(self):
		response = self.client.post('/users/create/', {'username':'jr', 'password':'password'}, format='json')
		self.assertEqual(response.status_code, 200)

		response_obj = json.loads(response.content.decode('utf-8'))
		#self.assertEqual(response_obj['token'], Token.objects.get(user=user.user).key)
	
	def test_username_exists(self):
		user = make_user('jr', 'password')
		response = self.client.post('/users/create/', {'username':'jr', 'password':'password'}, format='json')
		self.assertEqual(response.status_code, 200)

		response_obj = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response_obj['error'], 'Username already exists')

	def test_missing_fields(self):
		response = self.client.post('/users/create/', {}, format='json')
		self.assertEqual(response.status_code, 401)
