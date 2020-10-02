from django.db import models

# Create your models here.
class Adherent(models.Model):
    score = models.CharField(max_length=30, null=True)
