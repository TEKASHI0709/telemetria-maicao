from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RolViewSet, RecursoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'recursos', RecursoViewSet, basename='recursos')

urlpatterns = [
    path('', include(router.urls)),
]