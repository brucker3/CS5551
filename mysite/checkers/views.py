from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Adherent



# Create your views here.
@login_required(login_url='login')
def homeview (request):
    return render(request, 'checkers/home.html')

def signupview (request):
    form = SignupForm()

    if (request.method == 'POST'):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            return redirect('login')
            messages.success(request, "registration successful")
    context={'form':form}
    return render(request, 'checkers/signup.html',context)

def loginview (request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'incorrect informations')
    context={}
    return render(request,'checkers/login.html',context)

def logoutview(request):
    logout(request)
    return redirect('login')
