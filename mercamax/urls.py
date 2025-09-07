from django.contrib import admin
from django.urls import path, include
from users.views import LoginView, Verify2FAView, ValidateTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    #APIs de módulos de negocio
    path('api/inventario/', include('inventario.urls')),
    path('api/bodega/', include('bodega.urls')),

    #APIs de usuarios
    path('api/users/', include('users.urls')),

    # Autenticación principal
    path('api/auth/login/', LoginView.as_view(), name='custom-login'),
    path('api/auth/verify-2fa/', Verify2FAView.as_view(), name = 'verify-2fa'),
    path('api/auth/validate-token/', ValidateTokenView.as_view(), name = 'validate-token'),

    #dj-rest-auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
