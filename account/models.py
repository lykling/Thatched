#-*- coding=utf-8 -*-
from django.db import models
from md5 import md5

# Create your models here.

class UserProfile(models.Model):
	uid				= models.AutoField(primary_key=True)
	avatar			= models.ImageField(upload_to="avatar",null=True,blank=True)
	nickname		= models.CharField(max_length=16, null=True)
	realname		= models.CharField(max_length=39, null=True)
	sns				= models.URLField(null=True)
	regip			= models.IPAddressField()
	intro			= models.CharField(max_length=20, null=True)

class User(models.Model):
	uid				= models.AutoField(primary_key=True)
	username		= models.CharField(max_length=16)
	password		= models.CharField(max_length=32)
	email			= models.EmailField(null=True)
	profile			= models.OneToOneField(UserProfile)
	def __unicode__(self):
		return self.username
	def md5pwdequal(self, slat, opwd):
		return bool(md5(self.password + slat).hexdigest() == opwd)
	def classelector(self):
		return [(x.classid, x.classname) for x in self.classification_set.all()]

class Group(models.Model):
	gid				= models.AutoField(primary_key=True)
	groupname		= models.CharField(max_length=16)
	members			= models.ManyToManyField(User)
	def __unicode__(self):
		return self.groupname

class AuthSession(models.Model):
	sessionid		= models.CharField(max_length=32)
	slat			= models.CharField(max_length=16)
