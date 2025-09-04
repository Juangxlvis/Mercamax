from django.shortcuts import render

# users/views.py

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response

from .permissions import IsAdminUser
from .serializers import InviteUserSerializer
from core.models import PerfilUsuario
from .serializers import ActivateAccountSerializer


class InviteUserView(generics.CreateAPIView):
    """
    Vista para que un administrador invite a un nuevo usuario al sistema.
    """
    permission_classes = [IsAdminUser]
    serializer_class = InviteUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Crear el usuario como inactivo y sin contraseña usable
        try:
            user = User.objects.create(
                username=data['email'],
                email=data['email'],
                first_name=data['first_name'],
                is_active=False
            )
            user.set_unusable_password()
            user.save()

            # 2. Asignar el perfil y el rol
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rol = data['rol']
            perfil.save()

            # 3. Generar token y link de activación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://localhost:4200/activar-cuenta/{uid}/{token}" # URL del frontend

            # 4. Enviar el correo
            send_mail(
                '¡Bienvenido a MercaMax! Activa tu cuenta',
                f'Hola {user.first_name},\n\nPor favor, haz clic en el siguiente enlace para activar tu cuenta y establecer tu contraseña:\n\n{activation_link}\n\nGracias,\nEl equipo de MercaMax.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({'detail': 'Invitación enviada exitosamente.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # En caso de un error inesperado, borrar el usuario si se alcanzó a crear
            if 'user' in locals() and user.pk:
                user.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ActivateAccountView(generics.GenericAPIView):
    """
    Endpoint para activar la cuenta de un usuario invitado.
    """
    permission_classes = [] # Es un endpoint público
    serializer_class = ActivateAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data.get('uid')
        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('password')

        try:
            # Decodificar el UID para obtener el ID del usuario
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Verificar que el usuario exista y que el token sea válido
        if user is not None and default_token_generator.check_token(user, token):
            # Activar el usuario y establecer su contraseña
            user.is_active = True
            user.set_password(password)
            user.save()
            return Response({'detail': 'Cuenta activada exitosamente.'}, status=status.HTTP_200_OK)
        else:
            # Si el token no es válido o el usuario no existe
            return Response({'error': 'El enlace de activación no es válido.'}, status=status.HTTP_400_BAD_REQUEST)

