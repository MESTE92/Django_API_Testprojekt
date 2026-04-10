from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  # generische Views
from rest_framework.permissions import IsAuthenticated                                # eingeloggt?
from django.contrib.auth import get_user_model                                        # gibt CustomUser zurück

from .serializers import RegisterSerializer, UserProfileSerializer                    # Die Serializer
from .permissions import IsOwner                                                      # Custom Permission

User = get_user_model()                                                               # == CustomUser zur Laufzeit


class RegisterView(ListCreateAPIView):
    serializer_class = RegisterSerializer
    queryset         = User.objects.all()
    # keine permission_classes – jeder darf sich registrieren


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class   = UserProfileSerializer
    queryset           = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]  # eingeloggt + eigenes Profil