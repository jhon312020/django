from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

# User listing view
def index(request):
	user_list = User.objects.order_by('id')[:5]
	context = {'user_list': user_list}
	return render(request,'users/index.html',context)

# User registration
def register(request):
	return render(request, 'users/register.html')

# User login authentication
def login(request):
	return render(request, 'users/login.html')

# To create a new user 
# and return a token
def user_create(request):
	if request.method == 'POST':
		userName = request.POST['username']
		userPass = request.POST['password']
		user_exists = User.objects.filter(username = userName)
		if user_exists:
			content = {'error_message':'Username already exists'}
		else:
			# Creating user
			user = User.objects.create_user(userName, None, userPass)
			user.save()
			# Creating rest framework token
			token = Token.objects.create(user=user)
			if user.id:
				content = {'success_message':'Registered Successfully!', 'token':token.key}
			else:
				content = {'error_message':'Try after some time'}
	return JsonResponse(content)
	
# Validates the username and passwords
# and returns the stored token
def validate(request):
	if request.method == 'POST':
		userName = request.POST['username']
		userPass = request.POST['password']
		# Validating the user using auth function
		user = authenticate(username=userName, password=userPass)
		if user is not None:
			# Getting the stored rest framework token
			token = Token.objects.get(user=user)
			content = {'success_message':'Logged in Successfully!', 'token':token.key}
		else:
			content = {'error_message':'Invalid username/password'}
	return JsonResponse(content)
