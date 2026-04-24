from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # generische Klassen für CRUD-Operationen
from rest_framework.response import Response 
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from .serializers import CategorySerializer, ProductSerializer, JobSerializer         # Die Serialisier
from .models import Category, Product, Jobs                                                # Die Model-Klassen
from .pagination import CategoryPagination, ProductPagination, JobPagination            # Die Paginierungsklassen
from .throttle import CustomAnonRateThrottle, CustomUserRateThrottle                    # Die Custom Throttle-Klassen

from django.contrib.auth.models import User, Group



# Alle Kategorien (GET) + neue Kategorie (POST)
class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer              # jede Viewklasse braucht einen Serializer
    pagination_class = CategoryPagination
    queryset         = Category.objects.all()           # und ein Queryset das die Daten aus einem Model holt





# GET alle Produkte (mit Filter/Suche/Sortierung) + POST neues Produkt erstellen
class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticatedOrReadOnly]            # Authentifizierung für die CRUD-Operationen nötig

    filterset_fields = ['active', 'category', 'category__name']          # Filter für exakte Suchwerte zb. ?active=true
    ordering_fields  = ['price', 'name', 'category__name']               # Custom Sortierung wenn die Parameter in der URL angegeben sind
    search_fields    = ['name', 'description', 'sku', 'category__name']  # Globale Suche über mehrere Felder

    # category__name -> FK-Feld -> z.B. ?category__name=Kleidung  über einen Join in der DB

    def get_queryset(self):
        queryset = Product.objects.select_related('category')   # holt zu jedem Produkt auch die Kategorie per Join
                                                                # -> schneller und effizienter, weniger DB-Aufrufe
                                                                # (Queryset-Optimierung)

        name = self.request.query_params.get('name')                # .get('name') ist nur der URL-Parameter für
        description = self.request.query_params.get('description')  # eigene Filter
        sku = self.request.query_params.get('sku')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')


        # prüft ob der Parameter in der URL angegeben ist, falls ja wird der Filter
        # über eine AND-Verknüpfung angewendet -> so wird schrittweise der Query gefiltert

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





 # GET einzelnes Produkt + PUT/PATCH + DELETE
class ProductDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    queryset         = Product.objects.select_related('category')

    # kein get_queryset() nötig -> DRF holt Objekt automatisch per pk aus der URL



class JobListCreateView(ListCreateAPIView):
    serializer_class = JobSerializer
    pagination_class = JobPagination
    permission_classes = [IsAuthenticated]            # Authentifizierung für die CRUD-Operationen nötig

    filterset_fields = ['name', 'salary']
    ordering_fields  = ['salary', 'name']
    search_fields    = ['name']

    def get_queryset(self):
        queryset = Jobs.objects.all()
        name = self.request.query_params.get('name')
        salary = self.request.query_params.get('salary')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if salary:
            queryset = queryset.filter(salary__gte=salary)

        return queryset

class JobDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    queryset         = Jobs.objects.all()
    permission_classes = [IsAuthenticated]
    
    
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Authentifizierung für diese Funktion nötig
def app_manager_view(request):
    if request.user.groups.filter(name='Admingruppe').exists():  # zusätzlich prüfen ob der User in der Gruppe 'app_manager' ist
        return render(request, 'app_manager.html')
    else:
        raise PermissionDenied("Du hast keine Berechtigung, diese Seite zu sehen.")
    

@api_view(['GET'])
@throttle_classes([AnonRateThrottle])  # Throttling für diese Funktion, limitiert die Anzahl der Anfragen pro User/IP
def throttle_check(request):
    return Response({"message": "Throttling funktioniert!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Authentifizierung für diese Funktion nötig
@throttle_classes([UserRateThrottle])  # Throttling für diese Funktion, limitiert die Anzahl der Anfragen pro authentifiziertem User
def throttle_check_auth(request):
    return Response({"message": "Throttling funktioniertmit höheren Raten für authentifizierte User!"})


# TODO: cumstom anon function 

# TODO: custoim auth function


