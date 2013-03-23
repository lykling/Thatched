#-*- coding=utf-8 -*-
from django import forms
from article.models import *
#from ckeditor.widgets import CKEditor
from ckeditor.widgets import CKEditorWidget
#from tinymce import models as tinymce_models


class BlogPostForm(forms.ModelForm):
	classid			= forms.ChoiceField(label="Classification")
	subtitle		= forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':	'SubTitle',
		}))
	class Meta:
		model = Article
		fields = ('title', 'subtitle', 'content')
		widgets = {
			'title':	forms.TextInput(attrs={'placeholder':'Title'}),
			'content':	CKEditorWidget(),
			'subtitle':	forms.TextInput(attrs={'placeholder':'SubTitle'})
		}
	#subtitle = forms.CharField(widget=CKEditorWidget(config_name='none_toolbar'))
	#subtitle = forms.CharField()
	#tags			= forms.CharField(widget=CKEditorWidget(config_name='none_toolbar'))
