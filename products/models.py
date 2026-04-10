
from django.db import models

class Category(models.Model):                 # das Model Category
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorien'

    def __str__(self):
        return self.name




class Product(models.Model):                  # das Model Product
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    stock       = models.IntegerField(default=0)
    active      = models.BooleanField(default=True)
    sku         = models.CharField(max_length=50, unique=True)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)   #Bilderpfad
    category    = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

                                                            # related_name='products' ist ein Alias für die Beziehung,
                                                            # es erlaubt die Produkte von der Kategorie aus zu finden
                                                            # zb. kategorieprodukte = Kategorie.products.all()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'category']
        indexes = [
            models.Index(fields=['sku']),  # oft gesucht -> Index sinnvoll
            models.Index(fields=['active']),  # oft gefiltert -> Index sinnvoll
            models.Index(fields=['category']),  # FK -> oft gefiltert
            models.Index(fields=['name']), # nach Name filteren
        ]
        ordering = ['-active', 'category', 'name','price']   # Standardsortierung in dieser Reihenfolge wenn in
                                                            # der URL keine Sortierung angegeben ist -> siehe Views.py

        verbose_name = 'Produkt'    # Anzeige in Adminpannel bei einem Produkt
        verbose_name_plural = 'Produkte'   # Anzeige in Adminpannel bei mehreren Produkten




class Jobs(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['name', 'salary']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

        ordering = ['-salary', 'name']

        indexes = [
            models.Index(fields=['salary']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


