from django.shortcuts import render, redirect, get_object_or_404    # NEW
from django.contrib.auth import get_user_model                    # gibt CustomUser zurück
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser       # NEW - für Datei-Uploads per Formular

from .serializers import RegisterSerializer, UserProfileSerializer
from .permissions import IsOwner

User = get_user_model()


class RegisterView(ListCreateAPIView):
    serializer_class = RegisterSerializer
    queryset         = User.objects.all()
    parser_classes   = [MultiPartParser, FormParser]                 # Formular + Datei-Upload

    def get(self, request, *args, **kwargs):
        # GET -> Template rendern
        return render(request, 'users/register.html')

    def post(self, request, *args, **kwargs):
        # POST -> Serializer verarbeitet Daten
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return render(request, 'users/register.html', {
                'success': 'Registrierung erfolgreich! Du kannst dich jetzt anmelden.'
            })

        # Fehler an Template zurückgeben
        return render(request, 'users/register.html', {
            'errors': serializer.errors
        })


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class   = UserProfileSerializer
    queryset           = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes     = [MultiPartParser, FormParser]               # Formular + Datei-Upload

    def get(self, request, *args, **kwargs):
        # GET -> Profil des eingeloggten Users rendern
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(request, user)                 # IsOwner prüfen
        return render(request, 'users/profile.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(request, user)

        # Löschen wenn action=delete
        if request.data.get('action') == 'delete':
            user.delete()
            return redirect('register')

        # Update – partial=True erlaubt PATCH-ähnliches Verhalten (nicht alle Felder Pflicht)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return render(request, 'users/profile.html', {
                'user': user,
                'success': 'Profil erfolgreich gespeichert.'
            })

        return render(request, 'users/profile.html', {
            'user': user,
            'errors': serializer.errors
        })




class LoginView(APIView):                                   # kein Serializer nötig – Django auth übernimmt
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)  # prüft Credentials

        if user is not None:
            login(request, user)                            # Session erstellen
            return redirect('profile', pk=user.pk)         # weiterleiten zum Profil

        return render(request, 'users/login.html', {
            'error': 'Benutzername oder Passwort falsch.'
        })




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)                                     # Session beenden
        return redirect('login')


