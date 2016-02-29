from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import logging
import json

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

logging.basicConfig()
logger = logging.getLogger(__name__)

# Create your views here.

# Used to show a welcome message to user
# via httpresponse
def index(request):
	return HttpResponse("Welcome to user application!")

# Endpoint is Used for user login verification
# Returns a token as a result
# on successful validation
# Endpoint url : /users/authenticate

class AuthenticateView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))

		username = params.get('username')
		password = params.get('password')

		if username is None or password is None:
			return Response(status=401)

		try:
			user = authenticate(username=username, password=password)
			if user is not None:
				token, _ = Token.objects.get_or_create(user=user)
				return Response({'token':token.key})
			return Response({'message':'Invalid username/password or account doesn\'t exists'})
		except Exception as exception:
			logger.error(exception)
			return Response(status=500)

# Endpoint is Used to create a new user 
# Returns a authentication token as a result
# on successful creation
# Endpoint url : /users/create

class CreateView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		params = json.loads(request.body.decode('utf-8'))

		username = params.get('username')
		password = params.get('password')

		if username is None or password is None:
			return Response(status=401)
		user_exists = User.objects.filter(username = username)
		if user_exists:
			return Response({'error': 'Username already exists'})

		try:
			#user = User.objects.get(username=username, password=password)
			user = User.objects.create_user(username, None, password)
			user.save()
			token = Token.objects.create(user=user)
			return Response({'token':token.key})
		except User.DoesNotExist:
			# For security purposes, the user not existing returns
			# the same code as invalid credentails
			logger.info('Some server issue try after sometimes!')
			return Response(status=401)
		except Exception as exception:
			logger.error(exception)
			return Response(status=500)
