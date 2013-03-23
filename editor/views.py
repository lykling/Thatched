#-*- coding=utf-8 -*-
from account.functions import *

# Create your views here.

def editor_main(request):
	return render_to_response('main.html', {
		
	},context_instance=RequestContext(request))
