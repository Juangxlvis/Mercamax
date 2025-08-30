from django.db import models

# bodega/models.py (modelo Ubicacion actualizado)

class CategoriaUbicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    class TipoUbicacion(models.TextChoices):
        BODEGA = 'BODEGA', 'Bodega'
        ESTANTE_BODEGA = 'EST_BOD', 'Estante de Bodega'
        ESTANTE_TIENDA = 'EST_TDA', 'Estante de Tienda'

    nombre = models.CharField(max_length=200, unique=True)
    tipo = models.CharField(max_length=10, choices=TipoUbicacion.choices)
    
    # CAMPO AÑADIDO:
    categoria = models.ForeignKey(
        CategoriaUbicacion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Categoría de productos permitidos en esta ubicación (ej: Refrigerados)"
    )
    
    capacidad_maxima = models.PositiveIntegerField(null=True, blank=True, help_text="Capacidad en unidades o volumen")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_ubicaciones')

    def __str__(self):
        return self.nombre
    
class Lote(models.Model):
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='lotes')
    codigo_lote = models.CharField(max_length=100, unique=True, help_text="Código o número de remisión del proveedor")
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    fecha_caducidad = models.DateField()
    costo_compra_lote = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} - Lote {self.codigo_lote}"
    

class StockItem(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='stock_items')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='stock_items')
    cantidad = models.PositiveIntegerField()

    class Meta:
        # Asegura que solo haya un registro para un lote en una ubicación
        unique_together = ('lote', 'ubicacion')

    def __str__(self):
        return f"{self.cantidad} de {self.lote} en {self.ubicacion}"
    
