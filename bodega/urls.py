# bodega/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaUbicacionViewSet, UbicacionViewSet, LoteViewSet, StockItemViewSet

router = DefaultRouter()
router.register(r'categorias-ubicacion', CategoriaUbicacionViewSet, basename='categoria-ubicacion')
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'stockitems', StockItemViewSet, basename='stockitem')

urlpatterns = [
    path('', include(router.urls)),
]