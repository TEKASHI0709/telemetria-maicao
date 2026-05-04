from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Alert.objects.all().order_by('-created_at')
        return Alert.objects.filter(tank__owner=user).order_by('-created_at')