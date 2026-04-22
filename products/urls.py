
from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView, ProductDetailView, app_manager_view  # die Views
from .views import JobListCreateView, JobDetailView

app_name = 'products'  # Namespace -> verhindert Konflikte mit möglichen anderen Apps

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    # GET  /api/categories/   -> alle Kategorien
    # POST /api/categories/   -> neue Kategorie erstellen

    path('products/', ProductListCreateView.as_view(), name='product-list'),
    # GET  /api/products/     -> alle Produkte (mit Filter/Suche/Sortierung)
    # POST /api/products/     -> neues Produkt erstellen

    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # GET    /api/products/1/ -> einzelnes Produkt
    # PUT    /api/products/1/ -> Produkt komplett ersetzen
    # PATCH  /api/products/1/ -> Produkt teilweise ändern
    # DELETE /api/products/1/ -> Produkt löschen

    path('jobs/', JobListCreateView.as_view(), name='job-list'),
    # GET  /api/jobs/   -> alle Jobs (mit Filter/Suche/Sortierung)
    # POST /api/jobs/   -> neue Jobs erstellen

    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    # GET    /api/jobs/1/ -> einzelner Job
    # PUT    /api/jobs/1/ -> Job komplett ersetzen
    # PATCH  /api/jobs/1/ -> Job teilweise ändern
    # DELETE /api/jobs/1/ -> Job löschen
    
    path('app-manager/', app_manager_view, name='app-manager'),  # Beispiel für eine Funktion-basierte View
    # GET /api/app-manager/ -> Zugriff auf diese Funktion, Authentifizierung nötig
]