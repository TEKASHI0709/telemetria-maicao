from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Tank
from .serializers import TankSerializer

User = get_user_model()


class TankViewSet(viewsets.ModelViewSet):
    serializer_class = TankSerializer
    permission_classes = [IsAuthenticated]

    def get_impersonated_user(self):
        """Si el admin está impersonando a un usuario, devuelve ese usuario."""
        user = self.request.user
        is_admin = user.is_superuser or user.roles.filter(nombre='Administrador').exists()
        
        if not is_admin:
            return None
        
        impersonate_id = self.request.headers.get('X-Impersonate-User')
        if impersonate_id:
            try:
                return User.objects.get(id=impersonate_id)
            except User.DoesNotExist:
                return None
        return None

    def get_queryset(self):
        user = self.request.user
        impersonated = self.get_impersonated_user()
        
        if impersonated:
            return Tank.objects.filter(owner=impersonated)
        
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Tank.objects.all()
        return Tank.objects.filter(owner=user)

    def perform_create(self, serializer):
        impersonated = self.get_impersonated_user()
        owner = impersonated if impersonated else self.request.user
        serializer.save(owner=owner)