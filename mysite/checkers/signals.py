
"""
I adapted some code found at
@ inspired by: https://www.youtube.com/watch?v=Kc1Q_ayAeQk
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Adherent


def create_adherent(sender, instance, created, **kwargs):

    if created:
        try:
            Adherent.objects.create(user=instance)
        except:
            pass

post_save.connect(create_adherent, sender=User)
