
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  # Die generischen Views
from rest_framework.filters import OrderingFilter                                     # Die Filter
from django_filters.rest_framework import DjangoFilterBackend                         # Das Filter Backend
from .serializers import CategorySerializer, ProductSerializer                        # Die Serialisier
from .models import Category, Product                                                 # Die Model-Klassen


# Alle Kategorien (GET) + neue Kategorie (POST)
class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer              # jede Viewklasse braucht einen Serializer
    queryset         = Category.objects.all()           # und ein Queryset das die Daten aus einem Model holt





# GET alle Produkte (mit Filter/Suche/Sortierung) + POST neues Produkt erstellen
class ProductListCreateView(ListCreateAPIView):

    serializer_class = ProductSerializer
    filter_backends  = [DjangoFilterBackend, OrderingFilter]

    # DjangoFilterBackend  -> aktiviert exakte Filter per filterset_fields
    #                      -> ?active=true, ?category=1
    #
    # OrderingFilter       -> aktiviert Sortierung per ordering_fields
    #                      -> ?ordering=price, ?ordering=-name

    filterset_fields = ['active', 'category']      # Filter für exakte Suchwerte zb. ?active=true
    ordering_fields  = ['price', 'name', 'category__name']      # Custom Sortierung wenn die Parameter in der URL angegeben sind

    # category__name -> FK-Feld -> z.B. ?category__name=Kleidung  über einen Join in der DB

    def get_queryset(self):
        queryset = Product.objects.select_related('category')   # holt zu jedem Produkt auch die Kategorie per Join
                                                                # -> schneller und effizienter, weniger DB-Aufrufe
                                                                # (Queryset-Optimierung)
        search    = self.request.query_params.get('search')

        ######################### globaler Filter nach einem Suchbegriff #########################
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(sku__icontains=search) |
                Q(category__name__icontains=search)
                        # category__name -> FK-Join -> sucht im Kategorienamen
                        # Q() -> OR -> Treffer in einem der Felder reicht,
                        # Q() kapselt Filterbedingungen
            )

        ########################### Gezielte Suche bei mehreren Suchbegriffen  ###########################
        # -> jeder weitere Parameter,
        # schränkt das Queryset weiter ein -> AND

        name = self.request.query_params.get('name')                # .get('name') ist nur der URL-Parameter
        description = self.request.query_params.get('description')
        sku = self.request.query_params.get('sku')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if sku:
            queryset = queryset.filter(sku__icontains=sku)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

        ########################### Filterung Ende ###########################




 # GET einzelnes Produkt + PUT/PATCH + DELETE
class ProductDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    queryset         = Product.objects.select_related('category')

    # kein get_queryset() noetig -> DRF holt Objekt automatisch per pk aus der URL