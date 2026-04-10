from django.urls import path                         # für URL-Definitionen
from .views import RegisterView, UserProfileView, LoginView, LogoutView     # die Views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # POST – Registrierung


    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # GET/PUT/PATCH/DELETE – Profil

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
]