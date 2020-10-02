from django.contrib import admin
from django.urls import path
from .views import homeview,signupview, loginview,logoutview

urlpatterns = [
    path('', homeview, name='home'),
    path('signup/',signupview, name='signup'),
    path('login/',loginview, name='login'),
    path('logout/',logoutview, name='logout'),

]
