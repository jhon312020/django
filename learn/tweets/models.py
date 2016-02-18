from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tweets(models.Model):
	tweet_text = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

class Tweet_media(models.Model):
	tweet_text = models.CharField(max_length=150)
	tweet_media = models.CharField(max_length=150)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

