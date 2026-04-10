
from django.contrib.auth.models import AbstractUser     #für das Custom User Model
from django.db import models

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