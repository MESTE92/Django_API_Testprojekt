# Django REST API Testprojekt

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.0.3-green)
![DRF](https://img.shields.io/badge/DRF-3.17.1-red)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-lightgrey)

Ein Django-Testprojekt mit REST API für Produkt-, Kategorie- und Benutzerverwaltung, inklusive Token-Authentifizierung, Filterfunktionen, Suchoptionen und Admin-Panel.

## Screenshots

<p align="center">
  <img src="Beispielbilder/bidl_1.png" alt="API Browsable Interface" width="30%">
  <img src="Beispielbilder/bild_2.png" alt="API Response Example" width="30%">
  <img src="Beispielbilder/API_Doku.png" alt="Interactive API Documentation" width="30%">
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
- [Geschützte vs. öffentliche Endpunkte](#geschützte-vs-öffentliche-endpunkte)
- [Admin-Panel](#admin-panel)
- [Projektstruktur](#projektstruktur)
- [Nächste Schritte](#nächste-schritte)
- [Wichtige Dateien zum Lesen](#wichtige-dateien-zum-lesen)
- [Notizen](#notizen)
- [Kurzanleitung](#kurzanleitung)
- [Empfohlene Betrachtungsweise](#empfohlene-betrachtungsweise)

---

## Features

- **RESTful API** mit Django REST Framework
- **Produkt- und Kategorieverwaltung** mit vollständigem CRUD
- **Job-Verwaltung** mit Gehaltsfeldern und Sortierung
- **Benutzerverwaltung**:
  - Registrierung mit Passwort-Validierung (Groß-/Kleinbuchstaben, Zahl, Sonderzeichen)
  - XSS-Schutz durch `bleach`-Sanitierung aller Texteingaben
  - Profilbild-Upload (ImageField)
  - Öffentliche Profilansicht (Benutzername + Profilbild)
  - Automatische Token-Erstellung bei Registrierung (via `post_save`-Signal)
  - Session-basierter Login/Logout
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

Das Projekt enthält eine vollständige Benutzerverwaltung unter dem Präfix `/api/users/`.

### Endpunkte

| Endpunkt | Methode | Beschreibung | Auth erforderlich |
|----------|---------|--------------|:-----------------:|
| `http://127.0.0.1:8000/api/users/register/` | GET | Registrierungs-Formular anzeigen | Nein |
| `http://127.0.0.1:8000/api/users/register/` | POST | Neuen Benutzer registrieren | Nein |
| `http://127.0.0.1:8000/api/users/login/` | GET | Login-Formular anzeigen | Nein |
| `http://127.0.0.1:8000/api/users/login/` | POST | Einloggen (Session) | Nein |
| `http://127.0.0.1:8000/api/users/logout/` | POST | Ausloggen | Ja |
| `http://127.0.0.1:8000/api/users/profile/<pk>/` | GET | Eigenes Profil anzeigen | Ja (nur Eigentümer) |
| `http://127.0.0.1:8000/api/users/profile/<pk>/` | POST | Profil bearbeiten oder löschen | Ja (nur Eigentümer) |
| `http://127.0.0.1:8000/api/users/profile/<pk>/public/` | GET | Öffentliches Profil ansehen | Ja |

### Registrierung

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
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

> **Hinweis**: Bei der Registrierung wird automatisch ein Auth-Token erstellt und der Session-Login ist sofort möglich.

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -F "username=MeinName" \
  -F "password=MeinPasswort1!"
```

### Token-Authentifizierung

Jeder Benutzer bekommt bei der Registrierung automatisch einen Token zugewiesen. Den Token findest du im Django Admin-Panel unter **Tokens** (`http://127.0.0.1:8000/admin/authtoken/token/`).

Token in Requests verwenden:

```bash
curl http://127.0.0.1:8000/api/users/profile/1/public/ \
  -H "Authorization: Token <dein-token>"
```

---

## Geschützte vs. öffentliche Endpunkte

| Endpunkt | Zugriff |
|----------|---------|
| `GET /api/products/` | Öffentlich |
| `GET /api/categories/` | Öffentlich |
| `POST/PUT/DELETE /api/products/` | Öffentlich (Dev-Modus) |
| `GET /api/users/register/` | Öffentlich |
| `POST /api/users/register/` | Öffentlich |
| `GET/POST /api/users/login/` | Öffentlich |
| `POST /api/users/logout/` | Eingeloggt |
| `GET/POST /api/users/profile/<pk>/` | Eingeloggt + Eigentümer |
| `GET /api/users/profile/<pk>/public/` | Eingeloggt |

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
**Viel Erfolg beim Testen!**
