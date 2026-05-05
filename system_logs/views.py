from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import SystemLog
from .serializers import SystemLogSerializer


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SystemLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Solo el admin puede ver los logs del sistema
        is_admin = user.is_superuser or user.roles.filter(nombre='Administrador').exists()
        if not is_admin:
            raise PermissionDenied('Solo el administrador puede ver los logs del sistema.')
        
        return SystemLog.objects.all().order_by('-created_at')[:200]