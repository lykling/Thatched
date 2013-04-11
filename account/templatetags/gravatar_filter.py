# -*- coding: UTF-8 -*-
from django import template
import urllib, hashlib
from django.template import Library
from django.template.defaultfilters import stringfilter
register = Library()
@stringfilter
def gravatar(value, arg):
	"""
	transform email to gravatar.
	"""
	size = 200
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(value.lower()).hexdigest() + "?"
	try:
		currsize = int(arg)
	except ValueError: # Invalid literal for int().
		pass
	else:
		size = currsize
	gravatar_url += urllib.urlencode({'s':str(size)})
	return gravatar_url

gravatar.is_safe = True
register.filter('gravatar', gravatar)
