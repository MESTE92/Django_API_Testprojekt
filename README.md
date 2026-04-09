# Django REST API Testprojekt

Ein vollständiges Django-Testprojekt mit REST API für Produkt- und Kategorienverwaltung, inklusive Filterfunktionen, Suchoptionen und Admin-Panel.

---

## Inhaltsverzeichnis

- [Features](#features)
- [Technologie-Stack](#technologie-stack)
- [Installation & Setup](#installation--setup)
- [Datenbank mit Testdaten befüllen](#datenbank-mit-testdaten-befüllen)
- [Server starten](#server-starten)
- [API testen](#api-testen)
- [Admin-Panel](#admin-panel)
- [Projektstruktur](#projektstruktur)

---

## Features

- **RESTful API** mit Django REST Framework
- **Produkt- und Kategorieverwaltung** mit vollständigem CRUD
- **Erweiterte Suchfunktionen**:
  - Globale Suche über mehrere Felder
  - Gezielte Filterung (Name, SKU, Preis, Kategorie, Status)
  - Preisbereich-Filter (min_price, max_price)
  - Sortierung nach verschiedenen Feldern
- **Django Admin-Panel** zur Verwaltung
- **Vorkonfigurierte Testdaten** zum sofortigen Ausprobieren
- **Formatunterstützung**: JSON, XML, CSV

---

## Technologie-Stack

- **Backend**: Django 6.0.3
- **API**: Django REST Framework 3.17.1
- **Datenbank**: SQLite3 (Standard)
- **Filter**: django-filter
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
- 5 Kategorien (Technik, Lebensmittel, Kleidung, Haushalt, Sport)
- Mehrere Beispielprodukte mit unterschiedlichen Preisen, SKUs und Lagerbeständen

> **TIPP**: Die Fixture-Datei enthält realistische Testdaten, um die API-Funktionen direkt ausprobieren zu können.

---

## Server starten

Starte den Django-Entwicklungsserver:

```bash
python manage.py runserver
```

Der Server läuft standardmäßig auf: **http://127.0.0.1:8000/**

---

## API testen

Die Datei `test_requests.txt` enthält vorkonfigurierte URLs zum Testen aller API-Funktionen.

### Hauptendpunkte

| Endpunkt | Beschreibung |
|----------|--------------|
| `http://127.0.0.1:8000/api/products/` | Alle Produkte abrufen |
| `http://127.0.0.1:8000/api/products/1/` | Einzelnes Produkt (ID: 1) |
| `http://127.0.0.1:8000/api/categories/` | Alle Kategorien abrufen |

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
http://127.0.0.1:8000/api/products/?category=1
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

## Admin-Panel

Zugriff auf das Django Admin-Panel: **http://127.0.0.1:8000/admin/**

### Standard-Credentials (siehe `hints.txt`)

```
E-Mail: Admin@Test.de
Passwort: Admin1234!
```

**Im Admin-Panel kannst du:**
- Produkte erstellen, bearbeiten und löschen
- Kategorien verwalten
- Produktbilder hochladen
- Lagerbestände anpassen
- Produkte aktivieren/deaktivieren

---

## Projektstruktur

```
Projekt_mit_API/
│
├── products/                      # Haupt-App für Produkte und Kategorien
│   ├── fixtures/
│   │   └── initial_data.json     # Testdaten zum Importieren
│   ├── migrations/                # Datenbank-Migrationen
│   ├── models.py                  # Product & Category Models
│   ├── serializers.py             # DRF Serializers
│   ├── views.py                   # API Views
│   ├── urls.py                    # API URL-Routing
│   └── admin.py                   # Admin-Konfiguration
│
├── Testprojekt/                   # Hauptprojekt-Konfiguration
│   ├── settings.py                # Django Settings
│   ├── urls.py                    # Haupt-URL-Konfiguration
│   └── wsgi.py                    # WSGI-Konfiguration
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
5. **Teste die API** mit den URLs aus `test_requests.txt`
6. **Erkunde das Admin-Panel** unter `/admin/`

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

---

**Viel Erfolg beim Testen!**
