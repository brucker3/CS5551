# checkers/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Adherent
from checkers import  board
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
import logging
logger = logging.getLogger("mylogger")

# Create your views here.
@login_required(login_url='login')
def homeview (request):
    return render(request, 'checkers/home.html')


#------------------------------
#-------registration---------
#------------------------------
class signupview (FormView):
    template_name = 'checkers/signup.html'
    form_class = SignupForm
    success_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            messages.success(request, "registration successful, please login to access your space")
            return redirect('login')
        return render(request, self.template_name, {'form': form})

#------------------------------
#-------login view---------
#------------------------------
class loginview (FormView):
    template_name = 'checkers/login.html'
    form_class = LoginForm
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'incorrect informations')
            return redirect('login')
        #context={}
        #return render(request,'checkers/login.html',context)

#------------------------------
#-------logout view---------
#------------------------------

class logoutview(View):
    def get(self, request):
        logout(request)
        return redirect('login')

# def logoutview(request):
#     logout(request)
#     return redirect('login')

class rulesview(View):
    def get(self, request):
        return render(request, 'checkers/rules.html')

class player_statsview(View):
    def get(self, request):
        return render(request, 'checkers/player_stats.html')


class game(View):
    print("test of board build class")

    def get(self, request):
        if request.method == 'GET':
            return HttpResponse(render(request,'checkers/game.html'))
			
    def room(request, room_name):
        return render(request, 'game/room.html', {
            'room_name': room_name
        })		
	
##	