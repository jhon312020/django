from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('username', 'password')
		password = serializers.CharField(write_only=True)

	def create(self, validated_data):
		user = User(
			username=validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		Model = Group
		fields = ('url', 'name')
