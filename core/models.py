from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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

class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        STOCK_BAJO = 'STOCK', 'Stock Bajo'
        LOTE_VENCE = 'VENCE', 'Lote por Vencer'

    usuario_destino = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta para {self.usuario_destino.username}: {self.mensaje}"

# También es un buen lugar para poner la "señal" que crea el perfil automáticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)