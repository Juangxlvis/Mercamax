from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a administradores (Gerente o superuser).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Permite el acceso si es un superusuario o si tiene el rol de Gerente.
        return request.user.is_superuser or (
            hasattr(request.user, 'perfilusuario') and 
            request.user.perfilusuario.rol == 'GERENTE_SUPERMERCADO'
        )