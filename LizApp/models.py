from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Diary(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=1000,null="True",default="My Diary")
	def __str__(self):
		return str(self.id) + " - " + self.author.username


class Entry(models.Model):
	diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
	timeDate = models.DateTimeField(auto_now_add=True)
	details = models.TextField()
	day = models.CharField(max_length=20)
	def __str__(self):
		return str(self.id) + " - " + self.diary.name


class Wallet(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	balance = models.BigIntegerField(default=0)
	name = models.CharField(max_length=1000,null="True",default="My Wallet")
	no_cred = models.IntegerField(default=0)
	no_deb = models.IntegerField(default=0)
	def __str__(self):
		return str(self.id) + " - " + self.owner.username


class Transaction(models.Model):
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)
	tType = models.CharField(max_length=1)
	def __str__(self):
		return str(self.id) + " - " + self.waller.name
