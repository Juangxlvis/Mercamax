from django.shortcuts import render

from rest_framework import viewsets
from .models import CategoriaUbicacion, Ubicacion, Lote, StockItem
from .serializers import (
    CategoriaUbicacionSerializer, UbicacionSerializer, 
    LoteSerializer, StockItemSerializer
)

class CategoriaUbicacionViewSet(viewsets.ModelViewSet):
    queryset = CategoriaUbicacion.objects.all()
    serializer_class = CategoriaUbicacionSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer