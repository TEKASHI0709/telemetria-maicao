from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reading
from .serializers import ReadingSerializer


class ReadingViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Reading.objects.all().order_by('-timestamp')
        return Reading.objects.filter(tank__owner=user).order_by('-timestamp')