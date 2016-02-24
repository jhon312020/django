from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import UserSerializer, GroupSerializer

# Create your views here.

def create(self, validated_data):
	user = User(
		username=validated_data['username']
	)
	user.set_password(validated_data['password'])
	user.save()
	return user

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
class GroupViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows users to viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

