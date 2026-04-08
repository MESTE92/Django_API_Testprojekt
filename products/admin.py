from django.contrib import admin
from .models import Product, Category


# die Modelle werden hier registriert zur Verwaltung im Adminbereich

admin.site.register(Product)
admin.site.register(Category)
