from django.contrib import admin
from django.urls import path
from .views import *
#homeview,signupview, loginview,logoutview

urlpatterns = [
    path('', homeview, name='home'),
    path('signup/',signupview.as_view(), name='signup'),
    path('login/',loginview.as_view(), name='login'),
    path('logout/',logoutview.as_view(), name='logout'),
    path('game/', game.as_view(), name='game'),
    path('rules', rulesview.as_view(), name='rules'),
    path('player_stats', player_statsview.as_view(), name='player_stats'),

]
