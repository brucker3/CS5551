from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Adherent


def create_profile(sender, instance, created, **kwargs):

    if created:
        try:
            Adherent.objects.create(user=instance)
        except:
            pass

post_save.connect(create_profile, sender=User)
