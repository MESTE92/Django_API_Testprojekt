# Django REST API Testprojekt

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.0.3-green)
![DRF](https://img.shields.io/badge/DRF-3.17.1-red)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-lightgrey)

Ein Django-Testprojekt mit REST API für Produkt-, Kategorie- und Benutzerverwaltung, inklusive Token-Authentifizierung, Filterfunktionen, Suchoptionen und Admin-Panel.

## Screenshots

### API & Dokumentation

<p align="center">
  <img src="Beispielbilder/bidl_1.png" alt="API Browsable Interface" width="30%">
  <img src="Beispielbilder/bild_2.png" alt="API Response Example" width="30%">
  <img src="Beispielbilder/API_Doku.png" alt="Interactive API Documentation" width="30%">
</p>

### Benutzeroberfläche

<p align="center">
  <img src="Beispielbilder/Homepage.png" alt="Homescreen" width="30%">
  <img src="Beispielbilder/Homepage_2.png" alt="Homescreen (eingeloggt)" width="30%">
  <img src="Beispielbilder/Login.png" alt="Login-Seite" width="30%">
</p>
<p align="center">
  <img src="Beispielbilder/Registrierung.png" alt="Registrierungs-Seite" width="30%">
  <img src="Beispielbilder/User.png" alt="Benutzerprofil" width="30%">
</p>

---

## Inhaltsverzeichnis

- [Features](#features)
- [Technologie-Stack](#technologie-stack)
- [Installation & Setup](#installation--setup)
- [Datenbank mit Testdaten befüllen](#datenbank-mit-testdaten-befüllen)
- [Server starten](#server-starten)
- [API-Dokumentation](#api-dokumentation)
- [API testen](#api-testen)
- [User- & Authentifizierungs-API](#user---authentifizierungs-api)
- [Benutzer über das Admin-Panel anlegen](#option-3--benutzer--token-komplett-über-das-admin-panel-anlegen)
- [Geschützte vs. öffentliche Endpunkte](#geschützte-vs-öffentliche-endpunkte)
- [Admin-Panel](#admin-panel)
- [Projektstruktur](#projektstruktur)
- [Nächste Schritte](#nächste-schritte)
- [Wichtige Dateien zum Lesen](#wichtige-dateien-zum-lesen)
- [Notizen](#notizen)
- [Kurzanleitung](#kurzanleitung)
- [Empfohlene Betrachtungsweise](#empfohlene-betrachtungsweise)
- [Djoser & JWT (implementiert, nicht aktiv)](#djoser--jwt-implementiert-nicht-aktiv)

---

## Features

- **RESTful API** mit Django REST Framework
- **Produkt- und Kategorieverwaltung** mit vollständigem CRUD
- **Job-Verwaltung** mit Gehaltsfeldern und Sortierung
- **Benutzerverwaltung mit UI**:
  - **Homescreen** mit Navigationslinks (Login, Registrierung, API-Docs)
  - Registrierung mit Passwort-Validierung (Groß-/Kleinbuchstaben, Zahl, Sonderzeichen)
  - Session-basierter Login/Logout mit Template-Oberfläche
  - Profilseite mit Bearbeiten-Funktion und Profilbild-Upload (ImageField)
  - Öffentliche Profilansicht (Benutzername + Profilbild, zugänglich für eingeloggte User)
  - XSS-Schutz durch `bleach`-Sanitierung aller Texteingaben
  - Automatische Token-Erstellung bei Registrierung (via `post_save`-Signal)
  - Token-Abruf per POST an `/api/auth/` (ohne Registrierungs-Flow)
- **Erweiterte Suchfunktionen**:
  - Globale Suche über mehrere Felder (`?search=`)
  - Gezielte Filterung (Name, SKU, Beschreibung, Preis, Kategorie, Status)
  - Filter nach Kategorie-ID oder Kategorie-Name (`?category=1` oder `?category__name=Technik`)
  - Preisbereich-Filter (`?min_price=` & `?max_price=`)
  - Sortierung nach verschiedenen Feldern (`?ordering=price`, `?ordering=-name`)
- **Pagination** (Seitenweise Anzeige):
  - Standard: 5 Einträge pro Seite
  - Anpassbare Seitengröße über URL-Parameter (`?page_size=`)
  - Separate Pagination-Einstellungen für Produkte (max: 100) und Kategorien (max: 10)
  - Kombinierbar mit verschiedenen Filter- und Suchfunktionen
- **Interaktive API-Dokumentation** mit Swagger/OpenAPI:
  - Automatisch generierte API-Dokumentation
  - Interaktive Testmöglichkeit direkt im Browser
  - OpenAPI 3.0 Schema-Export
- **Django Admin-Panel** zur Verwaltung
- **Vorkonfigurierte Testdaten** zum sofortigen Ausprobieren
- **Formatunterstützung**: JSON, XML, CSV

---

## Technologie-Stack

- **Backend**: Django 6.0.3
- **API**: Django REST Framework 3.17.1
- **Datenbank**: SQLite3 (Standard)
- **Filter**: django-filter
- **API-Dokumentation**: drf-spectacular (OpenAPI 3.0)
- **XSS-Schutz**: bleach
- **Authentifizierung (installiert, noch nicht aktiv genutzt)**: djoser + djangorestframework-simplejwt
- **Python**: 3.x

---

## Installation & Setup

### 1. Repository klonen

```bash
git clone <repository-url>
cd Projekt_mit_API
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
python -m venv .venv

# Auf macOS/Linux:
source .venv/bin/activate

# Auf Windows:
.venv\Scripts\activate
```

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

> **WICHTIG**: Überprüfe die `requirements.txt` für alle benötigten Pakete.

### 4. Umgebungsvariablen konfigurieren

Erstelle eine `.env` Datei im Hauptverzeichnis basierend auf der `.env.example`:

```bash
cp .env.example .env
```

**Bearbeite die `.env` Datei und trage die erforderlichen Werte ein:**

```env
SECRET_KEY='dein-generierter-secret-key'
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

> **Secret Key generieren**:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```
> Kopiere den generierten Key in deine `.env` Datei.

> **HINWEIS**: Lies die `.env.example` Datei für detaillierte Informationen zu den Konfigurationsoptionen.

### 5. Datenbank-Migrationen durchführen

```bash
python manage.py migrate
```

### 6. Superuser erstellen (für Admin-Panel)

```bash
python manage.py createsuperuser
```

Folge den Anweisungen oder nutze die vorkonfigurierten Credentials aus der `hints.txt`.

---

## Datenbank mit Testdaten befüllen

Das Projekt enthält vorkonfigurierte Testdaten in `products/fixtures/initial_data.json`.

### Testdaten importieren

```bash
python manage.py loaddata products/fixtures/initial_data.json
```

**Was wird importiert?**
- 10 Kategorien (Technik, Lebensmittel, Kleidung, Haushalt, Sport, Buecher, Spielzeug, Beauty, Garten, Buero)
- 200 Beispielprodukte mit unterschiedlichen Preisen, SKUs und Lagerbeständen

> **TIPP**: Die Fixture-Datei enthält realistische Testdaten, um die API-Funktionen direkt ausprobieren zu können.

---

## Server starten

Starte den Django-Entwicklungsserver:

```bash
python manage.py runserver
```

Der Server läuft standardmäßig auf: **http://127.0.0.1:8000/**

---

## API-Dokumentation

Das Projekt nutzt **drf-spectacular** für eine automatisch generierte, interaktive API-Dokumentation im Swagger/OpenAPI-Format.

### Interaktive Swagger-Dokumentation

Öffne die interaktive API-Dokumentation im Browser:

**http://127.0.0.1:8000/api/docs/**

![API Dokumentation](Beispielbilder/API_Doku.png)

**Was du hier tun kannst:**
- Alle verfügbaren Endpunkte durchsuchen
- Request/Response-Schemas ansehen
- API-Requests direkt im Browser testen (Try it out!)
- Parameter und Filter dokumentiert
- Beispiel-Responses für jeden Endpunkt

### OpenAPI Schema exportieren

Das vollständige OpenAPI 3.0 Schema ist verfügbar unter:

**http://127.0.0.1:8000/api/schema/**

Du kannst das Schema herunterladen und in Tools wie **Postman**, **Insomnia** oder anderen API-Clients importieren.

---

## API testen

Die Datei `test_requests.txt` enthält vorkonfigurierte URLs zum Testen aller API-Funktionen.

### Hauptendpunkte

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `http://127.0.0.1:8000/api/products/` | GET | Alle Produkte abrufen |
| `http://127.0.0.1:8000/api/products/1/` | GET | Einzelnes Produkt (ID: 1) |
| `http://127.0.0.1:8000/api/categories/` | GET | Alle Kategorien abrufen |

### Suchfunktionen

**Globale Suche** (durchsucht Name, Beschreibung, SKU, Kategorie):
```
http://127.0.0.1:8000/api/products/?search=laptop
http://127.0.0.1:8000/api/products/?search=Technik
```

**Gezielte Suche**:
```
http://127.0.0.1:8000/api/products/?name=laptop
http://127.0.0.1:8000/api/products/?sku=TECH
http://127.0.0.1:8000/api/products/?category=1              # Filter nach Kategorie-ID
http://127.0.0.1:8000/api/products/?category__name=Technik  # Filter nach Kategorie-Name
http://127.0.0.1:8000/api/products/?active=true             # Nur aktive Produkte
```

**Preisfilter**:
```
http://127.0.0.1:8000/api/products/?min_price=10&max_price=50
http://127.0.0.1:8000/api/products/?min_price=100
```

**Sortierung**:
```
http://127.0.0.1:8000/api/products/?ordering=price        # aufsteigend
http://127.0.0.1:8000/api/products/?ordering=-price       # absteigend
http://127.0.0.1:8000/api/products/?ordering=name
```

**Kombinierte Filter**:
```
http://127.0.0.1:8000/api/products/?search=laptop&ordering=-price
http://127.0.0.1:8000/api/products/?category=1&ordering=-price&active=true
```

**Pagination** (Seitenweise Anzeige):
```
http://127.0.0.1:8000/api/products/?page=1                # Seite 1 (Standard: 5 Einträge)
http://127.0.0.1:8000/api/products/?page=2                # Seite 2
http://127.0.0.1:8000/api/products/?page_size=10          # 10 Einträge pro Seite
http://127.0.0.1:8000/api/products/?page=2&page_size=20   # Seite 2 mit 20 Einträgen
http://127.0.0.1:8000/api/categories/?page=1&page_size=5  # Kategorien mit Pagination
```

**Pagination-Einstellungen**:
- **Produkte**: Standard 5 pro Seite, Maximum 100 pro Seite
- **Kategorien**: Standard 5 pro Seite, Maximum 10 pro Seite
- Bei ungültiger Seitenzahl wird automatisch die letzte Seite zurückgegeben

**Pagination kombiniert mit Filtern**:
```
http://127.0.0.1:8000/api/products/?category=1&page=1
http://127.0.0.1:8000/api/products/?category__name=Technik&page=1&page_size=5
http://127.0.0.1:8000/api/products/?search=laptop&page_size=3&ordering=-price
http://127.0.0.1:8000/api/products/?min_price=20&max_price=100&page=1
```

> **Vollständige Liste**: Öffne `test_requests.txt` für alle verfügbaren Testanfragen mit Beispielen.

### API im Browser testen

Django REST Framework bietet eine benutzerfreundliche Web-Oberfläche:
- Öffne einfach die URLs im Browser
- Du kannst direkt POST/PUT/DELETE Requests über die Weboberfläche ausführen

### API mit Tools testen

Alternativ kannst du Tools wie **Postman**, **Insomnia** oder **curl** verwenden:

```bash
curl http://127.0.0.1:8000/api/products/
```

---

## User- & Authentifizierungs-API

Das Projekt enthält eine vollständige Benutzerverwaltung mit Template-Oberfläche. Die Routen liegen direkt auf dem Root-Pfad (kein `/api/users/`-Präfix).

### Endpunkte

| Endpunkt | Methode | Beschreibung | Auth erforderlich |
|----------|---------|--------------|:-----------------:|
| `http://127.0.0.1:8000/` | GET | Homescreen | Nein |
| `http://127.0.0.1:8000/home/` | GET | Homescreen (alternativ) | Nein |
| `http://127.0.0.1:8000/register/` | GET | Registrierungs-Formular anzeigen | Nein |
| `http://127.0.0.1:8000/register/` | POST | Neuen Benutzer registrieren | Nein |
| `http://127.0.0.1:8000/login/` | GET | Login-Formular anzeigen | Nein |
| `http://127.0.0.1:8000/login/` | POST | Einloggen (Session) | Nein |
| `http://127.0.0.1:8000/logout/` | POST | Ausloggen | Ja |
| `http://127.0.0.1:8000/profile/<pk>/` | GET | Eigenes Profil anzeigen | Ja (nur Eigentümer) |
| `http://127.0.0.1:8000/profile/<pk>/` | POST | Profil bearbeiten oder löschen | Ja (nur Eigentümer) |
| `http://127.0.0.1:8000/profile/<pk>/edit/` | GET/POST | Profil bearbeiten (Edit-Formular) | Ja (nur Eigentümer) |
| `http://127.0.0.1:8000/profile/<pk>/public/` | GET | Öffentliches Profil ansehen | Ja |
| `http://127.0.0.1:8000/api/auth/` | POST | Token per Credentials abrufen | Nein |

### Homescreen

Der Homescreen unter `http://127.0.0.1:8000/` bietet eine Übersicht aller wichtigen Links:
- Login & Registrierung
- Link zur interaktiven API-Dokumentation
- Navigation zum eigenen Profil (wenn eingeloggt)

### Registrierung

Über die Weboberfläche unter `http://127.0.0.1:8000/register/` oder per curl:

```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -F "username=MeinName" \
  -F "email=email@example.com" \
  -F "password=MeinPasswort1!"
```

**Passwort-Anforderungen:**
- Mindestens 8 Zeichen
- Mindestens ein Großbuchstabe
- Mindestens ein Kleinbuchstabe
- Mindestens eine Zahl
- Mindestens ein Sonderzeichen (`!@#$%^&*` etc.)

> **Hinweis**: Bei der Registrierung wird automatisch ein Auth-Token erstellt. Nach der Registrierung erfolgt eine automatische Weiterleitung zur Login-Seite.

### Login & Session

Über die Weboberfläche unter `http://127.0.0.1:8000/login/` oder per curl:

```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -F "username=MeinName" \
  -F "password=MeinPasswort1!"
```

Nach erfolgreichem Login wird die Session gesetzt und der Benutzer zum eigenen Profil weitergeleitet.

### Logout

```bash
curl -X POST http://127.0.0.1:8000/logout/ \
  -H "Authorization: Token <dein-token>"
```

Nach dem Logout wird die Session beendet und der Benutzer zum Homescreen weitergeleitet.

### Token-Authentifizierung

#### Option 1 – Token per API abrufen (`/api/auth/`)

Sende einen POST-Request mit Benutzername und Passwort an den `api/auth/`-Endpunkt, um direkt einen Token zurückzubekommen – ohne den Registrierungs-Flow zu durchlaufen:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "MeinName", "password": "MeinPasswort1!"}'
```

**Antwort:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Dieser Token kann anschließend in jedem Request im `Authorization`-Header mitgeschickt werden:

```bash
curl http://127.0.0.1:8000/profile/1/public/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

#### Option 2 – Token im Admin-Panel einsehen

Jeder Benutzer bekommt bei der Registrierung automatisch einen Token zugewiesen. Den Token findest du im Django Admin-Panel unter **Tokens**:

**http://127.0.0.1:8000/admin/authtoken/token/**

#### Option 3 – Benutzer & Token komplett über das Admin-Panel anlegen

Falls du den Registrierungs-Flow überspringen möchtest, kannst du Benutzer und Token direkt im Admin-Panel anlegen:

1. Öffne **http://127.0.0.1:8000/admin/**
2. Gehe zu **Benutzer → Benutzer hinzufügen** und lege den neuen Benutzer an
3. Vergib Passwort, E-Mail und ggf. Berechtigungen direkt im Formular
4. Navigiere anschließend zu **Auth Token → Tokens → Token hinzufügen**
5. Wähle den neu angelegten Benutzer aus – der Token wird automatisch generiert und gespeichert
6. Der Token ist sofort aktiv und kann in API-Requests verwendet werden

> **Tipp**: Das Admin-Panel ist der schnellste Weg, um Test-User mit Tokens anzulegen, ohne die Registrierungsseite zu nutzen.

---

## Geschützte vs. öffentliche Endpunkte

| Endpunkt | Zugriff |
|----------|---------|
| `GET /` | Öffentlich (Homescreen) |
| `GET /home/` | Öffentlich (Homescreen) |
| `GET /api/products/` | Öffentlich |
| `GET /api/categories/` | Öffentlich |
| `POST/PUT/DELETE /api/products/` | Öffentlich (Dev-Modus) |
| `GET /register/` | Öffentlich |
| `POST /register/` | Öffentlich |
| `GET/POST /login/` | Öffentlich |
| `POST /api/auth/` | Öffentlich (Token per Credentials abrufen) |
| `POST /logout/` | Eingeloggt |
| `GET/POST /profile/<pk>/` | Eingeloggt + Eigentümer |
| `GET/POST /profile/<pk>/edit/` | Eingeloggt + Eigentümer |
| `GET /profile/<pk>/public/` | Eingeloggt |

---

## Admin-Panel

Zugriff auf das Django Admin-Panel: **http://127.0.0.1:8000/admin/**

### Anmeldung mit Standard-Credentials

Die vorkonfigurierten Admin-Zugangsdaten findest du in der `hints.txt`:

```
Username: Admin
E-Mail: Admin@Test.de
Passwort: Admin1234!
```

**So meldest du dich an:**
1. Öffne http://127.0.0.1:8000/admin/ in deinem Browser
2. Gib den Usernamen ein: `Admin`
3. Gib das Passwort ein: `Admin1234!`
4. Klicke auf "Log in"

### Eigenen Superuser erstellen

Falls die Standard-Credentials nicht funktionieren oder du einen eigenen Superuser anlegen möchtest:

```bash
python manage.py createsuperuser
```

**Du wirst nach folgenden Informationen gefragt:**
1. **Username**: Dein gewünschter Benutzername (z.B. `admin` oder dein Name)
2. **Email address**: Deine E-Mail-Adresse (z.B. `admin@example.com`)
3. **Password**: Dein Passwort (mindestens 8 Zeichen, wird beim Eingeben nicht angezeigt)
4. **Password (again)**: Passwort zur Bestätigung nochmal eingeben

**Beispiel:**
```bash
$ python manage.py createsuperuser
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**Anschließend kannst du dich mit deinen neuen Zugangsdaten unter http://127.0.0.1:8000/admin/ anmelden.**

### Was du im Admin-Panel tun kannst

**Im Admin-Panel kannst du:**
- Produkte erstellen, bearbeiten und löschen
- Kategorien verwalten
- Jobs verwalten
- Produktbilder hochladen
- Lagerbestände anpassen
- Produkte aktivieren/deaktivieren
- Benutzer und Berechtigungen verwalten
- Auth-Tokens einsehen (`/admin/authtoken/token/`)

---

## Projektstruktur

```
Projekt_mit_API/
│
├── products/                      # App für Produkte, Kategorien und Jobs
│   ├── fixtures/
│   │   └── initial_data.json     # Testdaten zum Importieren
│   ├── migrations/                # Datenbank-Migrationen
│   ├── models.py                  # Product, Category & Jobs Models
│   ├── serializers.py             # DRF Serializers
│   ├── views.py                   # API Views
│   ├── urls.py                    # API URL-Routing
│   ├── pagination.py              # Pagination-Konfiguration
│   └── admin.py                   # Admin-Konfiguration
│
├── users/                         # App für Benutzerverwaltung & Auth
│   ├── migrations/                # Datenbank-Migrationen
│   ├── models.py                  # CustomUser Model + Token-Signal
│   ├── serializers.py             # Register-, Profile- & Public-Serializer
│   ├── views.py                   # Register, Login, Logout, Profile Views
│   ├── urls.py                    # User URL-Routing
│   ├── permissions.py             # IsOwner Permission
│   └── admin.py                   # Admin-Konfiguration
│
├── Testprojekt/                   # Hauptprojekt-Konfiguration
│   ├── settings.py                # Django Settings (inkl. drf-spectacular Config)
│   ├── urls.py                    # Haupt-URL-Konfiguration (inkl. API-Docs)
│   └── wsgi.py                    # WSGI-Konfiguration
│
├── Beispielbilder/                # Screenshots für README
│   ├── bidl_1.png                 # API Browsable Interface
│   ├── bild_2.png                 # API Response Example
│   └── API_Doku.png               # Swagger-Dokumentation
│
├── manage.py                      # Django Management-Script
├── db.sqlite3                     # SQLite Datenbank
├── requirements.txt               # Python Dependencies
├── .env.example                   # Beispiel-Konfiguration
├── hints.txt                      # Admin-Zugangsdaten
├── test_requests.txt              # API-Test-URLs
└── README.md                      # Diese Datei
```

---

## Nächste Schritte

1. **Lies die `hints.txt`** für Admin-Zugangsdaten und wichtige Hinweise
2. **Überprüfe die `requirements.txt`** für alle installierten Pakete
3. **Konfiguriere deine `.env`** basierend auf `.env.example`
4. **Importiere Testdaten** mit `loaddata` Kommando
5. **Öffne die API-Dokumentation** unter http://127.0.0.1:8000/api/docs/
6. **Teste die API** mit den URLs aus `test_requests.txt`
7. **Erkunde das Admin-Panel** unter http://127.0.0.1:8000/admin/
8. **Registriere einen Testbenutzer** unter http://127.0.0.1:8000/api/users/register/

---

## Wichtige Dateien zum Lesen

| Datei | Zweck |
|-------|-------|
| `hints.txt` | Admin-Credentials und Zugangshinweise |
| `requirements.txt` | Alle Python-Dependencies |
| `.env.example` | Konfigurationsvorlage für Umgebungsvariablen |
| `test_requests.txt` | Vorgefertigte API-Test-URLs mit Beispielen |
| `products/fixtures/initial_data.json` | Testdaten für die Datenbank |

---

## Notizen

- **Development-Modus**: Dieses Projekt ist für Entwicklungs- und Testzwecke konfiguriert
- **Sicherheit**: Ändere SECRET_KEY und andere Credentials für Produktionsumgebungen
- **Datenbank**: SQLite wird verwendet (für Production PostgreSQL/MySQL empfohlen)
- **Dateiname**: `Beispielbilder/bidl_1.png` enthält einen Tippfehler im Dateinamen (nicht in der README)

---

## Kurzanleitung

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata products/fixtures/initial_data.json
python manage.py runserver
```

---

## Empfohlene Betrachtungsweise

- **Testprojekt / settings.py**
- **products / models.py**
- **products / admin.py**
- **products / serializers.py**
- **products / pagination.py**
- **products / views.py**
- **products / urls.py**
- **users / models.py**
- **users / serializers.py**
- **users / permissions.py**
- **users / views.py**
- **users / urls.py**
- **Testprojekt / urls.py**

---

## Djoser & JWT (implementiert, nicht aktiv)

Das Projekt hat **djoser** und **djangorestframework-simplejwt** installiert und konfiguriert – beide werden aktuell **nicht aktiv genutzt**. Das Projekt verwendet stattdessen seine eigene session-basierte Authentifizierung (Login/Logout/Register über Custom Views).

### Warum sind sie trotzdem enthalten?

Die Pakete sind als Vorbereitung für zukünftige API-Clients (z. B. mobile Apps oder ein React-Frontend) bereits eingebunden und konfiguriert, damit der Umstieg auf tokenbasierte Authentifizierung jederzeit ohne Installationsaufwand möglich ist.

### Verfügbare Endpunkte (aktuell nicht genutzt)

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/auth/token/login/` | POST | djoser: Token per Credentials abrufen |
| `/auth/token/logout/` | POST | djoser: Token invalidieren |
| `/api/auth/jwt/create/` | POST | simplejwt: Access- + Refresh-Token erstellen |
| `/api/auth/jwt/refresh/` | POST | simplejwt: Access-Token erneuern |
| `/api/auth/jwt/blacklist/` | POST | simplejwt: Refresh-Token auf Blacklist setzen |

### Konfiguration

Die JWT-Einstellungen sind in `Testprojekt/settings.py` unter `SIMPLE_JWT` hinterlegt:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    ...
}
```

> **Hinweis**: Die djoser-Endpunkte (`/auth/token/login/` und `/auth/token/logout/`) sind im URL-Namensraum von djoser und können zu Namenskonflikten mit den Custom-Views führen. Die Custom-Views nutzen daher den Namespace `users:` (z. B. `users:login`, `users:logout`), um eine saubere Trennung sicherzustellen.

---
**Viel Erfolg beim Testen!**
