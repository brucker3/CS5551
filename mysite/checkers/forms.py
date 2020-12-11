"""
I adapted some code found at
@ inspired by: https://djangosnippets.org/snippets/1723/
@ inspired by: https://gist.github.com/DrMartiner/ee93bd6fe1af4875f086f8396d13acd8
@ inspired by: https://docs.djangoproject.com/en/3.1/
@ inspired by: https://www.youtube.com/watch?v=Kc1Q_ayAeQk
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    class Meta:
        model = User
        fields = ('username','password')

class GuestForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super( GuestForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    class Meta:
        model = User
        fields = ('username',)
