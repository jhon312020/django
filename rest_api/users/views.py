from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token

from .models import Users

import hashlib

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def list(request):
	user_list = Users.objects.order_by('id')[:5]
	context = {'user_list': user_list}
	return render(request,'users/list.html',context)

def user_register(request):
	content = {}
	return render(request,'users/register.html',content)

def user_create(request):
	content = {}
	if request.method == 'POST':
		user_name = request.POST['username']
		password = request.POST['password']
		user_exists = Users.objects.filter(user_name = user_name)
		if user_exists:
			content = {'error_message':'Username already exists'}
		else:
			hashed_value = hashlib.sha1()
			hashed_value.update(user_name)
			hashed_value.update(password)
			password = hashed_value.hexdigest()
			user = Users(user_name = user_name, password = password )
			user.save()
			if user.id:
				content = {'success_message':'Registered Successfully!'}
			else:
				content = {'error_message':'Try after some time'}
	return JsonResponse(content)

#~ def user_create(request):
	#~ content = {}
	#~ if request.method == 'POST':
		#~ user_name = request.POST['username']
		#~ password = request.POST['password']
		#~ user_exists = Users.objects.filter(user_name = user_name)
		#~ if user_exists:
			#~ content = {'error_message':'Username already exists'}
		#~ else:
			#~ hashed_value = hashlib.sha1()
			#~ hashed_value.update(user_name)
			#~ hashed_value.update(password)
			#~ password = hashed_value.hexdigest()
			#~ user = Users(user_name = user_name, password = password )
			#~ user.save()
			#~ if user.id:
				#~ content = {'success_message':'Registered Successfully!'}
			#~ else:
				#~ content = {'error_message':'Try after some time'}
	#~ return render(request,'users/user_create.html',content)

def login(request):
	content = {}
	if request.method == 'POST':
		user_name = request.POST['username']
		password = request.POST['password']
		hashed_value = hashlib.sha1()
		hashed_value.update(user_name)
		hashed_value.update(password)
		password = hashed_value.hexdigest()
		user_exists = Users.objects.filter(user_name = user_name, password = password)
		if user_exists:
			content = {'success_message':'Login exists!'}
		else:
			content = {'error_message':'Invalid username or password'}
	return render(request,'users/login.html',content)
