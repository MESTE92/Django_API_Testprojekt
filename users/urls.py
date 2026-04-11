from django.urls import path                         # für URL-Definitionen
from .views import HomeView, RegisterView, UserProfileView, ProfileEditView, LoginView, LogoutView, UserPublicProfileView


urlpatterns = [
    path('', HomeView.as_view()),
    path('home/', HomeView.as_view(), name='home'),

    path('register/', RegisterView.as_view(), name='register'),
    # POST – Registrierung


    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # GET/PUT/PATCH/DELETE – Profil

    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    # GET/POST – Profil bearbeiten

    path('profile/<int:pk>/public/', UserPublicProfileView.as_view(), name='public_profile'),
    # GET – öffentliche Profilansicht (nur Benutzername + Profilbild)

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
]