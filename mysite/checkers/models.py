from django.db import models
from django.contrib.auth.models import User

from .board import Board
##COLORS##
DARK     = 'D' #bottom pieces
LIGHT      = 'L' #uppoer pieces
BLACK    = 'BLACK'
translation_dict = {};k =1;
for i in range(8):
	for j in range(8):
		if (((j+i))%2!=0):
			translation_dict[k]=[j,i]
			k+=1

# Create your models here.
class Adherent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)


class Game_Session(models.Model):
	game_id = models.CharField(max_length=255)
	game_object = models.TextField()
	player1_username = models.CharField(max_length=255)
	player2_username = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_open_to_join = models.BooleanField(default=True)
	
