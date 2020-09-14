from django.db import models

# Create your models here.

class Player(models.Model):
    nickname = models.CharField(max_length=30)

class Guest(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Adherent(models.Model):
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    routeoldgame = models.CharField(max_length=30)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    

class Game(models.Model):
    state = models.CharField(max_length=10)
    is_playing = models.BooleanField() 
    link_old_game = models.CharField(max_length=30)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Play(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)


class GameBoard(models.Model):
    number_pieces = models.IntegerField()
    positions = models.CharField(max_length=10)
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Piece(models.Model):
    color = models.CharField(max_length=20)
    row = models.IntegerField()
    column = models.IntegerField()
    is_crowned = models.BooleanField() 
    GameBoard = models.ForeignKey(GameBoard, on_delete=models.CASCADE)

class Rules(models.Model):
    is_move_valid = models.BooleanField(max_length=20)
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)



