from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Adherent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
