#-*- coding=utf-8 -*-
from account.functions import *
from account.forms import *
# Create your views here.

def login(request):
	errors = []
	if IsLogin(request):
		errors.append(u'You have already logged in.')
		return render_to_response('timeoutredirect.html', {
			'turl': '/index/',
			'timeout': '1000',
			'isLogin': IsLogin(request),
			'errors': errors,
		},context_instance=RequestContext(request))
	loginform = LoginForm()
	registerform = RegisterForm()
	slat = randomstr(5)
	#sessionid = md5(randomstr(27) + slat).hexdigest()
	if request.method == "POST":
		submit = request.POST.get('submit', '')
		if submit == "Login":
			loginform = LoginForm(request.POST)
			if loginform.is_valid():
				username = loginform.cleaned_data['username']
				password = loginform.cleaned_data['password']
				#session = AuthSession.objects.get(sessionid=sessionid_p)
				slat_p = request.session['slat']
				try:
					user = User.objects.get(username=username)
				except User.DoesNotExist:
					errors.append(u'Invalid username/email or passrod.')
				else:
					if user.md5pwdequal(slat=slat_p, opwd=password):
						request.session['user'] = user
						return HttpResponseRedirect("/")
					else:
						errors.append(u'Invalid username/email or password.')
				#session.delete()
				#assert False
		if submit == "Sign up":
			registerform = RegisterForm(request.POST)
			if registerform.is_valid():
				username = registerform.cleaned_data['username_reg']
				password = registerform.cleaned_data['password_reg']
				email = registerform.cleaned_data['email']
				confirm = registerform.cleaned_data['confirm']
				if not CharValid(username):
					errors.append(u"username contain invalid character.")
				if password != confirm:
					errors.append(u"Please check that your passwords match and try again.")
				if not errors:
					user = User.objects.create(
							username=username,
							password=password,
							email = email,
							profile = UserProfile.objects.create(nickname=username),
					)
					Classification.objects.create(creator=user,classname='unclassified')
					request.session['user'] = user
				return HttpResponseRedirect("/")
	loginform.fields['slat'].widget.attrs['value'] = slat
	request.session['slat'] = slat
	#loginform.fields['session'].widget.attrs['value'] = sessionid
	#AuthSession.objects.create(
		#slat = slat,
		#sessionid = sessionid
	#)
	return render_to_response('account/login.html', {
		'errors':		errors,
		'loginform':	loginform,
		'registerform':	registerform,
	},context_instance=RequestContext(request))

def logout(request):
	errors = []
	try:
		tpuser = request.session['user']
		del request.session['user']
	except KeyError:
		errors.append(u'You havn\'t logged in.')
	else:
		errors.append(u'Sign out successfuly.')
	return render_to_response('timeoutredirect.html', {
		'turl': '/index/',
		'timeout': '1000',
		'isLogin': IsLogin(request),
		'errors': errors,
	},context_instance=RequestContext(request))

def profile(request, uid):
	loginuser	= LoginUser(request)
	errors		= []
	form = ProfileForm(initial = {
		'nickname':		loginuser.profile.nickname,
		'realname':		loginuser.profile.realname,
		'sns':			loginuser.profile.sns,
		'intro':		loginuser.profile.intro,
		})
	if uid:
		user = User.objects.get(uid=uid)
		pass
	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				img = form.files['avatar']
			except KeyError:
				pass
			else:
				parser = ImageFile.Parser()
				for chunk in img.chunks():
					parser.feed(chunk)
				avatar = parser.close()
				path = "/var/www/blog/static/media/avatar"
				filename = "%d.png" % (loginuser.uid)
				avatar_s = Thumbnail(avatar, 120, 120, "%s/%s.s" % (path, filename))
				avatar_m = Thumbnail(avatar, 600, 600, "%s/%s.m" % (path, filename))
				avatar_b = Thumbnail(avatar, 2000,2000, "%s/%s.b" % (path, filename))
				tpw,tph = avatar.size
				if tpw > tph:
					box = ((tpw - tph) / 2, 0, (tpw + tph) / 2, tph)
				else:
					box = (0, (tph - tpw) / 2, tpw, (tph + tpw) / 2)
				avatar_p = CropImage(avatar, box, 120, "%s/%s.p" % (path, filename))
				loginuser.profile.avatar		= img
			loginuser.profile.sns			= form.cleaned_data['sns']
			loginuser.profile.nickname		= form.cleaned_data['nickname']
			loginuser.profile.realname		= form.cleaned_data['realname']
			loginuser.profile.intro			= form.cleaned_data['intro']
			loginuser.profile.save()
	return render_to_response('account/profile.html', {
		'errors':		errors,
		'loginuser':	loginuser,
		'form':			form,
	},context_instance=RequestContext(request))
