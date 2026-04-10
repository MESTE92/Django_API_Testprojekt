from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage


class CategoryPagination(PageNumberPagination):
    page_size = 5                        # Default: 5 Einträge pro Seite
    page_size_query_param = 'page_size'  # Parameter in URL: ?page_size=2
    max_page_size = 10                   # Maximum: maximal 10 Einträge erlaubt

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except EmptyPage:
            # Bei ungültiger Seite: automatisch letzte Seite zurückgeben
            paginator = Paginator(queryset, self.get_page_size(request))
            self.page = paginator.page(paginator.num_pages)
            return self.page.object_list





class ProductPagination(PageNumberPagination):
    page_size = 5                        # Default: 5 Einträge pro Seite
    page_size_query_param = 'page_size'  # Parameter in URL: ?page_size=20
    max_page_size = 100                  # Maximum: maximal 100 Einträge erlaubt

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except EmptyPage:
            # Bei ungültiger Seite: automatisch letzte Seite zurückgeben
            paginator = Paginator(queryset, self.get_page_size(request))
            self.page = paginator.page(paginator.num_pages)
            return self.page.object_list



class JobPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except EmptyPage:
            # Bei ungültiger Seite: automatisch letzte Seite zurückgeben
            paginator = Paginator(queryset, self.get_page_size(request))
            self.page = paginator.page(paginator.num_pages)
            return self.page.object_list






