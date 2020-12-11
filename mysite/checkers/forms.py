
# @ inspired by: https://docs.djangoproject.com/en/3.1/

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
