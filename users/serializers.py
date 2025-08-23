from rest_framework import serializers
from core.models import PerfilUsuario

class InviteUserSerializer(serializers.Serializer):
    """
    Serializer para validar los datos de la invitación de un nuevo usuario.
    """
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    rol = serializers.ChoiceField(choices=PerfilUsuario.ROLES)