
from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView, ProductDetailView  # die Views

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
]