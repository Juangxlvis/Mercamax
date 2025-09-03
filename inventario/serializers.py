# inventario/serializers.py
from rest_framework import serializers
from .models import Proveedor, Producto, CategoriaProducto
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

class ProductoSerializer(serializers.ModelSerializer):
    # 1. Definimos los nuevos campos que no existen en el modelo.
    stock_total = serializers.IntegerField(read_only=True)
    costo_promedio_ponderado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Producto
        # 2. Añadimos los nuevos campos a la lista de 'fields'.
        fields = [
            'id', 'nombre', 'codigo_barras', 'descripcion', 
            'precio_venta', 'stock_minimo', 'categoria', 'proveedor',
            'stock_total', 'costo_promedio_ponderado' 
        ]

    def to_representation(self, instance):
        """
        Sobreescribimos este método para añadir los cálculos al obtener los datos.
        """
        # Obtenemos la representación base (campos del modelo)
        data = super().to_representation(instance)
        
        # Cálculo del Stock Total
        stock_total = instance.lotes.aggregate(
            total=Sum('stock_items__cantidad')
        )['total'] or 0
        
        # Cálculo del Costo Promedio Ponderado
        valor_total_inventario = instance.lotes.aggregate(
            total_valor=Sum(F('stock_items__cantidad') * F('costo_compra_lote'))
        )['total_valor'] or 0

        if stock_total > 0:
            costo_promedio = valor_total_inventario / stock_total
        else:
            costo_promedio = 0

        # Añadimos los datos calculados a la respuesta
        data['stock_total'] = stock_total
        data['costo_promedio_ponderado'] = round(costo_promedio, 2)
        
        return data

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'