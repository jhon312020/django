from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import UserSerializer, GroupSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
serializer_class = UserSerializer
permission_classes = (permissions.AllowAny,)
def create(request):
	username = request.POST['username']
	password = request.POST['password']
	return HttpResponse("Username is " % (username, password))

def index(request):
	return render(request, 'users/index.html', '')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
	#~ def create(self, validated_data):
		#~ user = User(
			#~ username=validated_data['username']
		#~ )
		#~ user.set_password(validated_data['password'])
		#~ user.save()
		#~ return Token.objects.get_or_create(user=user)
	

class GroupViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows users to viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

