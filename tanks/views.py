from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tank
from .serializers import TankSerializer

class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    permission_classes = [IsAuthenticated]