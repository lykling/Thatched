#-*- coding=utf-8 -*-
from account.functions import *
from article.forms import *
# Create your views here.

def index(request):
	loginuser = LoginUser(request)
	return render_to_response('article/index.html', {
		'loginuser': loginuser,
	},context_instance=RequestContext(request))

def writeblog(request):
	loginuser = LoginUser(request)
	errors = []
	form = BlogPostForm()
	form.base_fields['classid'].choices = loginuser.classelector()
	form.fields['classid'].choices = loginuser.classelector()
	command = "create"
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		a = form.fields
		if form.is_valid():
			title		= form.cleaned_data['title']
			subtitle	= form.cleaned_data['subtitle']
			content		= form.cleaned_data['content']
			classid		= int(form.cleaned_data['classid'])
			articleid	= request.POST.get('articleid', '')
			command		= request.POST.get('command', '')
			if articleid and command == "modify":
				try:
					article = Article.objects.get(articleid=articleid)
				except Article.DoesNotExist:
					errors.append(u'article does not exist.')
				else:
					if article.author != loginuser:
						errors.append(u'you can\'t edit the article post by others.')
					else:
						article.title			= title
						article.subtitle		= subtitle
						article.content			= content
						article.classification	= Classification.objects.get(classid=classid)
						article.modifytime		= datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
						article.save()
						return HttpResponseRedirect("/leaves/%d/" % (article.articleid))
			elif command == "create":
				article = Article.objects.create(
						title			= title,
						subtitle		= subtitle,
						content			= content,
						author			= loginuser,
						classification	= Classification.objects.get(classid=classid),
						postime			= datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
						modifytime		= datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
				)
				return HttpResponseRedirect("/leaves/%d/" % (article.articleid))
	return render_to_response('article/writeblog.html', {
		'errors':		errors,
		'loginuser':	loginuser,
		'form':			form,	
		'command':		command,
	},context_instance=RequestContext(request))

def leaves(request, articleid=0):
	loginuser	= LoginUser(request)
	errors		= []
	if articleid:
		try:
			article = Article.objects.get(articleid=articleid)
		except Article.DoesNotExist:
			errors.append(u'Article Not Found')
		else:
			article.visit += 1
			article.save()
			form = BlogPostForm(initial={
				'classid':		loginuser.classelector(),
				'title':		article.title,
				'subtitle':		article.subtitle,
				'content':		article.content,
			})
			form.base_fields['classid'].choices = loginuser.classelector()
			form.fields['classid'].choices = loginuser.classelector()
			return render_to_response('article/leaves_specific.html', {
				'errors':		errors,
				'loginuser':	loginuser,
				'article':		article,
				'form':			form,
			},context_instance=RequestContext(request))
	return render_to_response('article/leaves.html', {
		'errors':		errors,
		'loginuser':	loginuser,
	},context_instance=RequestContext(request))

def getleaves(request):
	errors = []
	if request.method == "GET":
		command	= request.GET.get('command', '')
		number	= request.GET.get('number', '1')
		page	= request.GET.get('page', '1')
		uid		= request.GET.get('uid', '1')
		number	= int(number)
		page	= int(page)
		uid		= int(uid)
		if command == "newest":
			items = Article.objects.all()
		elif command == "userleaves":
			try:
				user	= User.objects.get(uid=uid)
			except User.DoesNotExist:
				errors.append(u'user does not exist.')
			else:
				items = user.article_set.all()
		if number <= 0:
			number = 1
		if (page - 1) * number > items.count() - 1:
			page = 1;
		if (page - 1) * number < 0:
			page = (items.count() - 1) / number + 1
	return render_to_response('article/getleaves.html', {
		'items':	items[number * (page - 1):number * page],
		'page':		page,
	},context_instance=RequestContext(request))

def getclassform(request):
	errors = []
	msgs = []
	classifies = []
	loginuser = LoginUser(request)
	if request.method == "GET":
		formname = request.GET.get('form_name', '')
	if request.method == "POST":
		formname	= request.POST.get('form_name', '')
		classname	= request.POST.get('classname', '')
		classid		= request.POST.get('classid', '')
		articleid	= request.POST.get('articleid', '')
		classifies	= request.POST.getlist('classifies[]', [])
		if formname == "create":
			if CharValid(classname) and classname != "unclassified" and classname != "":
				Classification.objects.create(
					creator		= loginuser,
					classname	= classname,
				)
				msgs.append(u'classification create successfuly.')
			else:
				errors.append(u'classname invalid.')
		elif formname == "moveto":
			if articleid:
				try:
					article = Article.objects.get(articleid=articleid)
				except Article.DoesNotExist:
					errors.append(u'article does not exist.')
				else:
					if article.author != loginuser:
						errors.append(u'you can\'t edit the article post by others.')
					else:
						try:
							article.classification = Classification.objects.get(classid=classid)
						except Classification.DoesNotExist:
							errors.append(u'class does not exist.')
						else:
							article.save()
							msgs.append(u'classification change successfuly.')
			else:
				errors.append(u'article not found.')
		elif formname == "delete":
			for classid in classifies:
				try:
					classification = Classification.objects.get(classid=classid)
				except Classification.DoesNotExist:
					errors.append(u'classification %s does no exist.' % (classid))
				else:
					if classification.creator == loginuser and classification.classname != "unclassified":
						for art in classification.article_set.all():
							art.classification = loginuser.classification_set.get(classname="unclassified")
							art.save()
						classification.delete()
						msgs.append(u'delete successfuly.')
					else:
						errors.append(u'you can\'t delete the classification created by others or delete the default classification.')
	return render_to_response('article/classform.html', {
		'errors':				errors,
		'msgs':					msgs,
		'loginuser':			loginuser,
		'formname':				formname,
		'classifies':			classifies,
	},context_instance=RequestContext(request))
