from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('username', 'password')
		password = serializers.CharField(write_only=True)

	#~ def perform_create(self, obj, created=False):
		#~ """
		#~ On creation, replace the raw password with a hashed version.
		#~ """
		#~ if created:
			#~ obj.set_password(obj.password)
			#~ obj.save()
#~ 
	#~ def create_hash(sender, instance=None, *args, **kwargs):
		#~ passwd = instance.password
		#~ instance.set_password(passwd)
		#~ pre_save.connect(create_hash, sender=User)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		Model = Group
		fields = ('url', 'name')
