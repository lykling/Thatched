from django.conf.urls import patterns, include, url 
from account.views import *
from article.views import *
from editor.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Thatched.views.home', name='home'),
    # url(r'^Thatched/', include('Thatched.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	#url(r'^tinymce/',include('tinymce.urls')),
	(r'^ckeditor/', include('ckeditor.urls')),
)

urlpatterns += patterns('article.views',
	(r'^$|^index/$', index),
	(r'^writting/$', LoginRequired(writeblog)),
	(r'^leaves/$|^leaves/(\d{1,8})/$', leaves),
	(r'^getleaves/$', getleaves),
	(r'^getclassform/$', getclassform),
	(r'^gettagsform/$', gettagsform),
)

urlpatterns += patterns('editor.views',
	(r'editor/$', editor_main),
)

urlpatterns += patterns('account.views',
	(r'^login/$', login),
	(r'^logout/$', LoginRequired(logout)),
	(r'^profile/$|^profile/(\d{1,8})/$', LoginRequired(profile)),
)

urlpatterns += patterns('account.functions',
	(r'^getpic/$', GetPic),
)

