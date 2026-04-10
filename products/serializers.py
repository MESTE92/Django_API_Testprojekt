import bleach                                          # für Datenbereinigung XSS
from rest_framework import serializers                 # für Serialisierung
from .models import Category, Product, Jobs            # Model-Klassen für Serialisierung

# Serialisierung der Kategorien
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category                                # Jeder Serializer braucht ein Model
        fields = ['id', 'name']                          # Felder die erialisiert werden sollen

        extra_kwargs = {
            'name': {'min_length': 3, 'required': True},
        }

    def validate(self, attrs):
        fields_to_validate = ['name']
        for field in fields_to_validate:
            if attrs.get(field):
                attrs[field] = bleach.clean(attrs[field])
        return attrs




# Serialisierung der Produkte
class ProductSerializer(serializers.ModelSerializer):
    # dieses Field bezieht sich per FK auf den Namen der Kategorie passend zum Produkt
    # read only -> wird nicht als Input erwartet
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model  = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'active',
            'sku',
            'image',
            'category',         # die FK-ID wird hier serialisiert
            'category_name',   # hier wird das Feld category_name dann serialisiert
        ]

        # Anpassungen an Standard-Validierungsregeln, jedes Feld kann exta Kriterien haben
        # zb. für Post oder Get Requests
        extra_kwargs = {
            'id':       {'read_only': True},
            'description': {'required': False},
            'name':     {'min_length': 3, 'required': True},
            'price':    {'min_value': 0.01, 'required': True},
            'sku':      {'required': True},
            'category': {'write_only': True},
            'category_name': {'read_only': True},
            'stock':    {'min_value': 0, 'required': True},
            'image':    {'required': False, 'allow_null': True},
            # write_only=True -> category ID nur als Input, nicht im JSON Output
        }


    # Schritt 1: Datenbereinigung
    def validate(self, attrs):   # eine Build in Methode vom DRF für Validierungen
        fields_to_validate = ['name', 'description','sku']  # Felder die potentiell XSS enthalten könnten
        for field in fields_to_validate:
            if attrs.get(field):    # Wenn das Feld im Request enthalten , also nicht leer ist...
                attrs[field] = bleach.clean(attrs[field])   # ... dann wird es hinsichtlich XSS bereinigt


        # Schritt 2: Zahlenfelder validieren
        if attrs['price'] <= 0:
            raise serializers.ValidationError("Der Preis muss groesser als 0 sein !")
        if attrs['stock'] < 0:
            raise serializers.ValidationError("Der Lagerbestand kann nicht negativ sein !")
        if attrs['stock'] > 5000:
            raise serializers.ValidationError("Der Lagerbestand darf maximal 5.000 Produkte betragen !")

        return attrs   # gibt die Validierungsergebnisse zurück




class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['id', 'name', 'salary', 'description']

        extra_kwargs = {
            'id': {'read_only': True},
            'description': {'required': False},
            'salary': {'min_value': 0.01, 'required': True},
            'name': {'min_length': 3, 'max_length': 255, 'required': True},
        }


    def validate(self, attrs):
        fields_to_validate = ['name', 'description']
        for field in fields_to_validate:
            if attrs.get(field):
                attrs[field] = bleach.clean(attrs[field])

        if attrs['salary'] <= 0:
            raise serializers.ValidationError("Das Gehalt muss groesser als 0 sein !")

        return attrs