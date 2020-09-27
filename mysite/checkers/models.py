from django.db import models

# Create your models here.
class Adherent(models.Model):
    email = models.CharField(max_length=30)
