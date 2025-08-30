# bodega/serializers.py
from rest_framework import serializers
from .models import CategoriaUbicacion, Ubicacion, Lote, StockItem

class CategoriaUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaUbicacion
        fields = '__all__'

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'