from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, index

# Router automático para ViewSet
router = DefaultRouter()
router.register(r'', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('frontend/', index, name='frontend'),
]
