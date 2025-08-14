# gestion/models.py
from django.db import models
from django.contrib.auth.models import User

# [cite_start]Modelo para los roles de usuario definidos en el documento [cite: 106, 99, 111, 116]
class PerfilUsuario(models.Model):
    ROLES = [
        ('CAJERO', 'Cajero'),
        ('ENCARGADO_INVENTARIO', 'Encargado de Inventario'),
        ('GERENTE_COMPRAS', 'Gerente de Compras'),
        ('GERENTE_SUPERMERCADO', 'Gerente del Supermercado'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

# [cite_start]Modelo para la entidad Proveedor [cite: 93]
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    contacto_nombre = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.nombre

# [cite_start]Modelo para los productos del inventario [cite: 68]
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_barras = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    costo_compra = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0) # Cantidad actual en inventario
    stock_minimo = models.PositiveIntegerField(default=10, verbose_name="Punto de Reorden") # Punto de reorden 
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT) # Cada producto tiene un proveedor
    
    def __str__(self):
        return self.nombre

# [cite_start]Modelo para el Proceso de Venta [cite: 201]
class Venta(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    cajero = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ventas_realizadas')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de la venta
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

# Modelo para el Proceso de Compra a Proveedores
class OrdenDeCompra(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    def __str__(self):
        return f"Orden #{self.id} a {self.proveedor.nombre}"

class DetalleOrdenDeCompra(models.Model):
    orden = models.ForeignKey(OrdenDeCompra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_solicitada = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)