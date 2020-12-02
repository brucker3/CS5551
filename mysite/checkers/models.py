from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Adherent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)



class Game_Session(models.Model):
	game_id = models.CharField(max_length=255, primary_key=True)
	game_object = models.TextField()
	player1_username = models.CharField(max_length=255)
	player2_username = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_open_to_join = models.BooleanField(default=True)

class Winner(models.Model):
    game = models.ForeignKey(Game_Session, on_delete=models.CASCADE, primary_key=True)
    winner_user = models.CharField(max_length=255)
