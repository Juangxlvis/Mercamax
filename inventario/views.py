# inventario/views.py
from rest_framework import viewsets
from .models import Proveedor, Producto
from .serializers import ProveedorSerializer, ProductoSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
