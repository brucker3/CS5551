# checkers/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from checkers import  board
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
import logging
from checkers import  players 
logger = logging.getLogger("mylogger")

from .game import Game
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.core import serializers
from django.db.models import Q
import pickle, codecs
global player_list
player_list = []
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
    logger.info(" sign up view running")
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            messages.success(request, "registration successful, please login to access your space")
            logger.info(" succesfully sign up redirect to login")
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
            global player_list
            login(request,user)
            new_player = players.Player(username)
            player_list.append(new_player)
            logger.info("sccessful login proceding to home page")
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
        logger.info("user log out")
        return redirect('login')


class rulesview(View):
    def get(self, request):
        logger.info(" routing to rules page")
        return render(request, 'checkers/rules.html')

class player_statsview(View):
    def get(self, request):
        logger.info("routing to stats page")
        return render(request, 'checkers/player_stats.html')


class game(View):
    logger.info("routing to game view")
    def get(self, request):
        open_to_join_games_data = {i.game_id:i.player1_username 
                                for i in Game_Session.objects.filter(
                                is_open_to_join=True
                                ).exclude(
                                player1_username = str(get_current_authenticated_user())
                                )} #active 1 means player is waiting for other player to join
        my_games_data = {i.game_id:[i.player1_username, i.player2_username] 
                                for i in Game_Session.objects.filter(
                                Q(player1_username = str(get_current_authenticated_user())) |
                                Q(player2_username = str(get_current_authenticated_user())) )}
        logger.info(open_to_join_games_data,my_games_data)
        if request.method == 'GET':
            return render(request,'checkers/game.html',{
                   'all_active_game_data':open_to_join_games_data,
                   'my_active_games': my_games_data,				   
            })
			   
    def room(request, game_id):
        logger.info("routing to game room")
        return render(request, 'game/room.html', {
            'game_id': game_id
        })		
	
    def create_game(request):
        new_game = Game()
        new_game.player1 = get_current_authenticated_user()
        all_game_ids = [i.game_id for i in Game_Session.objects.all()]
        while new_game.id in all_game_ids: # this while loop is to avoid game having same session id
            logger.info("regenerating new game id")
            new_game.regenerate_game_id()
        record = Game_Session(game_id=new_game.id, player1_username = new_game.player1, 
                              game_object = codecs.encode(pickle.dumps(new_game), "base64").decode())
        record.save()
        return redirect('/game/'+new_game.id)

    def join_game(request):
        if request.method == 'POST':
            selected_game_id = request.POST.get("game-id")
            print (selected_game_id)
            record_edit = Game_Session.objects.get(game_id=selected_game_id)
            print (dir(record_edit),record_edit, get_current_authenticated_user())
            record_edit.player2_username = str(get_current_authenticated_user())
            record_edit.is_open_to_join = False
            record_edit.save()
            logger.info("player joined game")
            return redirect('/game/'+selected_game_id)
    
    def resume_game(request):
        if request.method == "POST":
            selected_game_id = request.POST.get("game-id")
            logger.info("player resumed game")
            return redirect('/game/'+selected_game_id)			


class ai_game(View):
    def get(self, request):
        return render(request, 'checkers/ai_game.html')

    def start_game(reqeust):
    new_game = Game()
    player1 = get_current_authenticated_user()
    new_game.regnerate_game_id()
    # need to create instance of ai player and assigne to player 2 then rerout to game room 




