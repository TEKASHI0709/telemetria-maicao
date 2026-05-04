from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tank
from .serializers import TankSerializer


class TankViewSet(viewsets.ModelViewSet):
    serializer_class = TankSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # El admin ve todos los tanques, los demás solo los suyos
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Tank.objects.all()
        return Tank.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Al crear un tanque, se asigna automáticamente al usuario logueado
        serializer.save(owner=self.request.user)