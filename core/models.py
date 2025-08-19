from django.db import models
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

# También es un buen lugar para poner la "señal" que crea el perfil automáticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)