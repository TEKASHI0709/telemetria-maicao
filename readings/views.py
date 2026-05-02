from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reading
from .serializers import ReadingSerializer

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all().order_by('-timestamp')
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticated]