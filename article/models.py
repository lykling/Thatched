#-*- coding=utf-8 -*-
from django.db import models
from account.models import *

# Create your models here.

class Tag(models.Model):
	tagid			= models.AutoField(primary_key=True)
	tagname			= models.CharField(max_length=16)
	def __unicode__(self):
		return self.tagname

class Classification(models.Model):
	classid			= models.AutoField(primary_key=True)
	creator			= models.ForeignKey(User)
	classname		= models.CharField(max_length=16)
	def __unicode__(self):
		return self.classname

class Article(models.Model):
	articleid		= models.AutoField(primary_key=True)
	visit			= models.IntegerField(default=0)
	tags			= models.ManyToManyField(Tag, null=True)
	title			= models.CharField(max_length=256)
	subtitle		= models.CharField(max_length=526)
	classification	= models.ForeignKey(Classification)
	author			= models.ForeignKey(User)
	postime			= models.DateTimeField()
	modifytime		= models.DateTimeField()
	content			= models.TextField(max_length=32767)
	class Meta:
		ordering	= ['-postime']
	def tagselector(self):
		return [(x.tagid, x.tagname) for x in self.tags.all()]
