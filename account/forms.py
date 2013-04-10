#-*- coding=utf-8 -*-
from django import forms
from account.models import *
from ckeditor.widgets import CKEditorWidget


class LoginForm(forms.ModelForm):
	loginkeeping	= forms.BooleanField(required=False)
	class Meta:
		model = User
		fields = ('username', 'password')
		widgets = {
				'username':		forms.TextInput(attrs={
					'placeholder':	'username',
					'required':		'required',
					}),
				'password':		forms.PasswordInput(attrs={
					'placeholder':	'eg. "fj!5EY39',
					'required':		'required',
					}),
				'loginkeeping':	forms.CheckboxInput(attrs={
					'value':		'loginkeeping',
					})
				}

class RegisterForm(forms.ModelForm):
	username_reg	= forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':	'username',
		'required':		'required',
		}))
	password_reg = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':	'eg. "fj!5EY39',
		'required':		'required',
		}))
	confirm = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':	'eg. "fj!5EY39',
		'required':		'required',
		}))
	class Meta:
		model = User
		fields = ('email',)
		widgets = {
				'username':		forms.TextInput(attrs={
					'placeholder':	'username',
					'required':		'required',
					}),
				'password':		forms.PasswordInput(attrs={
					'placeholder':	'eg. "fj!5EY39',
					'required':		'required',
					}),
				'email':		forms.TextInput(attrs={
					'placeholder':	'mysupermail@mail.com',
					'required':		'required',
					'type':			'email',
					}),
				}

class ProfileForm(forms.ModelForm):
	avatar			= forms.ImageField(required=False)
	nickname		= forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder':	'Nickname',
		}))
	realname		= forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder':	'Realname',
		}))
	sns				= forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder':	'SNS',
		}))
	defaultemail	= forms.EmailField(required=False, widget=forms.TextInput(attrs={
		'placeholder':	'Email for public',
		}))
	intro			= forms.CharField(required=False, widget=forms.Textarea(attrs={
		'cols':			'39',
		'placeholder':	'Intro',
		}))
	password_old	= forms.CharField(required=False, widget=forms.PasswordInput(attrs={
		'placeholder':	'old password',
		}))
	password_new	= forms.CharField(required=False, widget=forms.PasswordInput(attrs={
		'placeholder':	'new password',
		}))
	password_cfm	= forms.CharField(required=False, widget=forms.PasswordInput(attrs={
		'placeholder':	'confirm password',
		}))
	semail			= forms.EmailField(required=False, widget=forms.TextInput(attrs={
		'placeholder':	'Email for security',
		}))
	class Meta:
		model = UserProfile
		fields = ('nickname', 'realname', 'sns', 'defaultemail', 'intro',)
