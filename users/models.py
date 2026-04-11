
from django.contrib.auth.models import AbstractUser     #für das Custom User Model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class CustomUser(AbstractUser):
    # Erbt: username, email, password, first_name, last_name, is_staff, etc. vom normalen User
    # Erweitert mit: Profile Picture Feld
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # Token automatisch erstellen – egal ob über Admin, register.html oder Shell
    if created:
        Token.objects.get_or_create(user=instance)