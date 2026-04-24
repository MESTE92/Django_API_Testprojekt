"""
URL configuration for Testprojekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin        # für die Admin Seite, die automatisch von Django generiert wird -> ermöglicht Datenbankeinträge über eine Weboberfläche zu verwalten

from django.conf import settings    # nötig für Zugriff auf alle Settings.py Variablen
from django.conf.urls.static import static  # generiert einen URL-Pattern der statische Dateien aus dem MEDIA_ROOT verarbeitet
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView   # für API Dokumentation mit drf-spectacular
from rest_framework.authtoken.views import obtain_auth_token                    # für Token Authentication (generiert einen Token, indem man Benutzernamen und Passwort an diesen Endpunkt sendet)
from rest_framework_simplejwt.views import (                        # für JWT Authentication (alternative zu Token Authentication)  
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('', include('users.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/', include('djoser.urls')),                                                  # Djoser Endpoints für User Registration, Login, Logout, Passwortänderung etc.
    path('auth/', include('djoser.urls.authtoken')),                                        # Djoser Endpoints für Token Authentication (z.B. Token erstellen, löschen)
    path('api/auth/', obtain_auth_token, name='api_token_auth'),                            # ermöglicht es, einen Token zu generieren, indem man Benutzernamen und Passwort an diesen Endpunkt sendet
    path('api/auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ermöglicht es, ein JWT (bestehend aus Access Token und Refresh Token) zu gener
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # ermöglicht es, ein neues Access Token zu generieren#, indem man ein gültiges Refresh Token an diesen Endpunkt sendet
    path('api/auth/jwt/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # ermöglicht es, ein Refresh Token zu invalidieren (z.B. bei Logout), indem man es an diesen Endpunkt sendet
]


# wird im DEBUG-Modus benutzt, in Produktionsumgebung übernimmt ein Webserver wie Nginx
# -> erstellt einen URL-Pattern:
            # /media/ -> BASE_DIR/media/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
