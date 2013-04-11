# -*- coding: UTF-8 -*-
### gravatar.py ###############
### place inside a 'templatetags' directory inside the top level of a Django app
###(not project, must be inside an app)
### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %}">
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below

from django import template
import urllib, hashlib
from django.template import Library
from django.template.defaultfilters import stringfilter


register = template.Library()
class GravatarUrlNode(template.Node):
	def __init__(self, email):
		self.email = template.Variable(email)

	def render(self, context):
		try:
			email = self.email.resolve(context)
		except template.VariableDoesNotExist:
			return ''

		#default = "/static/images/default.png.p"
		size = 220

		gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
		#gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
		gravatar_url += urllib.urlencode({'s':str(size)})

		return gravatar_url

@register.tag
def gravatar_url(parser, token):
	try:
		tag_name, email = token.split_contents()

	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

	return GravatarUrlNode(email)


register_filter = Library()
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
register_filter.filter('gravatar', gravatar)
