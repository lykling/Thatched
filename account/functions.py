#-*- coding=utf-8 -*-
from django.core.serializers import serialize,deserialize
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import connections
from account.models import *
from article.models import *
from random import randint
from md5 import md5 
import ImageFile
import datetime
import MySQLdb
import string
import random
import Image
import pytz
import time
import re
import os

invalidchar = "!<>*&^%$#`\"'|\\[{()}]?/,"

def randomstr(n):
	st = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	s = ''
	for i in range(n) :
		s += random.choice(st)
	return s

def IsLogin(request):
	return bool(request.session.get('user'))

def LoginRequired(view):
	def view_new(request, *args, **kwargs):
		if not IsLogin(request):
			return HttpResponseRedirect('/login/')
		return view(request, *args, **kwargs)
	return view_new

def LoginUser(request):
	try:
		return request.session['user']
	except KeyError:
		return None

def CharValid(text):
	for i in text:
		if i in invalidchar:
			return False
	return True

def StrToNum(text):
	nums = "0123456789"
	for i in text:
		if i not in nums:
			return 0
	return int(text)

def Thumbnail(image, width, height, path=None):
	img = image.copy()
	img.convert('RGB')
	img.thumbnail((width,height),Image.ANTIALIAS)
	img.format = image.format
	if path:
		img.save(path,image.format)
	return img

def ResizeImage(image, side, path=None):
	width, height = image.size
	if width > height:
		tmpw = side 
		tmph = int(height / (width*1.0 / tmph))
	else :
		tmph = side 
		tmpw = int(width / (height*1.0 / tmph))
	img = image.resize((tmpw, tmph), Image.ANTIALIAS)
	img.format = image.format
	if path:
		img.save(path,image.format)
	return img

def CropImage(image, box, scale=None, path=None):
	img = image.crop(box)
	img.format = image.format
	if scale:
		img = ResizeImage(img, scale)
		img.format = image.format
	if path:
		img.save(path,image.format)
	return img
