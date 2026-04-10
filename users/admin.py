from django.contrib import admin                    # importiert das Admin -Modul für @admin.register
from django.contrib.auth.admin import UserAdmin   # -> built-in Admin Interface für Hashing / Gruppen / Permissions etc.
from .models import CustomUser

@admin.register(CustomUser)                         # ->  entspricht: admin.site.register(CustomUser, CustomUserAdmin)
class CustomUserAdmin(UserAdmin):
    # Erbt das komplette built-in User Admin Interface
    # (Passwort-Hashing, Gruppenrechte, etc.)

    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {'fields': ('profile_picture',)}),  # neues Tab im Admin mit profile_picture

    )