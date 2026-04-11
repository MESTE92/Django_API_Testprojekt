from django.shortcuts import render, redirect, get_object_or_404   # get_object_or_404: Hilfsfunktion, die ein Objekt anhand von Kriterien abruft oder 404-Fehler zurückgibt
from django.contrib.auth import get_user_model                    # gibt CustomUser zurück
from django.contrib.auth import login, logout, authenticate       # login: erstellt Session, logout: beendet Session, authenticate: prüft Credentials
from rest_framework.views import APIView                           # Basis-View für benutzerdefinierte Logik (z.B. Login/Logout ohne Serializer)   
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser       # NEW - für Datei-Uploads per Formular

from .serializers import RegisterSerializer, UserProfileSerializer, UserPublicSerializer
from .permissions import IsOwner

User = get_user_model()


class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'users/home.html')


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
            return redirect('login')

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




class LoginView(APIView):                             # kein Serializer nötig – Django auth übernimmt
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
        return redirect('home')


class ProfileEditView(RetrieveUpdateDestroyAPIView):
    serializer_class   = UserProfileSerializer
    queryset           = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes     = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(request, user)
        return render(request, 'users/profile_edit.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(request, user)

        if request.data.get('action') == 'delete':
            user.delete()
            return redirect('register')

        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return render(request, 'users/profile_edit.html', {
                'user': user,
                'success': 'Profil erfolgreich gespeichert.'
            })

        return render(request, 'users/profile_edit.html', {
            'user': user,
            'errors': serializer.errors
        })


class UserPublicProfileView(RetrieveAPIView):               # Öffentliche Profilansicht (nur-lesen)
    serializer_class   = UserPublicSerializer
    queryset           = User.objects.all()
    permission_classes = [IsAuthenticated]                  # eingeloggt sein reicht – kein IsOwner

    def get(self, request, *args, **kwargs):
        profile_user = get_object_or_404(User, pk=kwargs['pk'])
        return render(request, 'users/public_profile.html', {'profile_user': profile_user})


