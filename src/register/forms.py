from django import forms
from .models import RegisterModel
from django.contrib.auth.models import User
class RegisterForm(forms.ModelForm):
	password = forms.CharField(max_length=255,widget=forms.PasswordInput)
	class Meta:
		model = RegisterModel
		fields =['name', 'username', 'email', 'password']
class SigninForm(forms.ModelForm):
	password = forms.CharField(max_length=255,widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['email', 'password']