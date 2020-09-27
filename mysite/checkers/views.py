from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Adherent
from operator import itemgetter


# Create your views here.
def homeview (request):
    return render(request, 'checkers/home.html')

def playerview (request):
    return render(request, 'checkers/playerview.html')

def signup (request):
    if request.method=="POST":
       nickname = request.POST['nickname']
       email = request.POST['email']
       password = request.POST['password']
    #check if nickname doesn't exist, then create the new player
    User.objects.create_user(username=nickname, password=password).save()
    lo = len(User.objects.all())-1
    Adherent(id = User.objects.all()[int(lo)].id, email=email).save()
    messages.add_message(request, messages.ERROR,"Sign Up Successful")
    return redirect('login')

    # check if nickname exist
    if User.objects.filter( username=nickname).exists():
        messages.add_message(request, messages.ERROR,"this nickname is already in use")
        return redirect('home')

def loginp (request):
    return render(request,'checkers/login.html')
