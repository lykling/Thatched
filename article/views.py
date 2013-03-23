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
	form = BlogPostForm()
	form.base_fields['classid'].choices = loginuser.classelector()
	form.fields['classid'].choices = loginuser.classelector()
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		a = form.fields
		if form.is_valid():
			title = form.cleaned_data['title']
			subtitle = form.cleaned_data['subtitle']
			content = form.cleaned_data['content']
			classid = int(form.cleaned_data['classid'])
			article = Article.objects.create(
				title			= title,
				subtitle		= subtitle,
				content			= content,
				author			= loginuser,
				classification	= Classification.objects.get(classid=classid),
				postime			= datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
			)
			return HttpResponseRedirect("/leaves/%d/" % (article.articleid))
	return render_to_response('article/writeblog.html', {
		'loginuser': loginuser,
		'form': form,	
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
	if request.method == "GET":
		command	= request.GET.get('command', '')
		number	= request.GET.get('number', '1')
		page	= request.GET.get('page', '1')
		number	= int(number)
		page	= int(page)
		items = Article.objects.all()
		if number <= 0:
			number = 1
		if (page - 1) * number > items.count() - 1:
			page = 1;
		if (page - 1) * number < 0:
			page = (items.count() - 1) / number + 1
		if command == "newest":
			return render_to_response('article/getleaves.html', {
				'items':	Article.objects.all()[number * (page - 1):number * page],
				'page':		page,
			},context_instance=RequestContext(request))
	return render_to_response('article/getleaves.html', {
	},context_instance=RequestContext(request))
