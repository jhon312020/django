from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Users(models.Model):
	user_name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.user_name