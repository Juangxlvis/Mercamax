# inventario/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proveedor, Producto
from .serializers import ProveedorSerializer, ProductoSerializer
from bodega.models import StockItem # Importamos StockItem
from bodega.serializers import StockDetailSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # --- NUEVA ACCIÓN PERSONALIZADA ---
    @action(detail=True, methods=['get'], url_path='stock-details')
    def stock_details(self, request, pk=None):
        """
        Endpoint para devolver la distribución detallada del stock
        de un producto específico en todas las ubicaciones.
        """
        # Buscamos el producto por su ID (pk)
        producto = self.get_object()
        
        # Buscamos todos los StockItems que pertenecen a los lotes de este producto
        queryset = StockItem.objects.filter(lote__producto=producto).order_by('ubicacion__nombre')
        
        # Usamos nuestro nuevo serializer para formatear los datos
        serializer = StockDetailSerializer(queryset, many=True)
        
        return Response(serializer.data)