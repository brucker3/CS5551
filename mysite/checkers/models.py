from django.db import models
from django.contrib.auth.models import User


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



from django_currentuser.db.models import CurrentUserField

class Foo(models.Model):
    created_by = CurrentUserField()