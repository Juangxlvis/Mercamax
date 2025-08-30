from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #APIs de módulos
    path('api/inventario/', include('inventario.urls')),
    path('api/users/', include('users.urls')),
    path('api/bodega/', include('bodega.urls')),
    # Rutas de autenticación
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('accounts/', include('allauth.urls')),
]
