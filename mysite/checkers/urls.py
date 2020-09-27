from django.contrib import admin
from django.urls import path
from .views import homeview, playerview, signup, loginp

urlpatterns = [
    path('', homeview, name='home'),
    path('signup/',signup),
    path('login/',loginp, name='login'),
    path('playerview/',playerview, name='playerview')
]
