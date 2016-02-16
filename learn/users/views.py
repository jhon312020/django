from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

def index(request):
	user_list = User.objects.order_by('id')[:5]
	context = {'user_list': user_list}
	return render(request,'users/index.html',context)

def register(request):
	return render(request, 'users/register.html')

def login(request):
	return render(request, 'users/login.html')

def user_create(request):
	if request.method == 'POST':
		userName = request.POST['username']
		userPass = request.POST['password']
		user_exists = User.objects.filter(username = userName)
		if user_exists:
			content = {'error_message':'Username already exists'}
		else:
			user = User.objects.create_user(userName, None, userPass)
			user.save()
			token = Token.objects.create(user=user)
			if user.id:
				content = {'success_message':'Registered Successfully!', 'token':token.key}
			else:
				content = {'error_message':'Try after some time'}
	return JsonResponse(content)

def validate(request):
	if request.method == 'POST':
		userName = request.POST['username']
		userPass = request.POST['password']
		user = authenticate(username=userName, password=userPass)
		#user_exists = User.objects.filter(username = userName)
		if user is not None:
			token = Token.objects.get(user=user)
			content = {'success_message':'Logged in Successfully!', 'token':token.key}
		else:
			content = {'error_message':'Invalid username/password'}
	return JsonResponse(content)
