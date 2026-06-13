from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reading
from .serializers import ReadingSerializer
from alerts.models import Alert
from tanks.models import Tank


class ReadingViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Reading.objects.all().order_by('-timestamp')
        return Reading.objects.filter(tank__owner=user).order_by('-timestamp')

    def perform_create(self, serializer):
        reading = serializer.save()
        self.generar_alertas(reading)

    def generar_alertas(self, reading):
        nivel = reading.level_percent
        tank = reading.tank

        # Verificar si ya existe una alerta activa del mismo tipo para este tanque
        def alerta_activa(tipo):
            return Alert.objects.filter(
                tank=tank,
                alert_type=tipo,
                is_read=False
            ).exists()

        # DESBORDAMIENTO: nivel mayor o igual a 95%
        if nivel >= 95:
            if not alerta_activa('OVERFLOW'):
                Alert.objects.create(
                    tank=tank,
                    alert_type='OVERFLOW',
                    message=f'⚠️ Tanque "{tank.name}" al {nivel:.1f}% - Riesgo de desbordamiento',
                    is_read=False
                )

        # NIVEL CRÍTICO: nivel menor a 20%
        elif nivel < 20:
            if not alerta_activa('CRITICAL'):
                Alert.objects.create(
                    tank=tank,
                    alert_type='CRITICAL',
                    message=f'🔴 Tanque "{tank.name}" en nivel crítico: {nivel:.1f}%',
                    is_read=False
                )

        # NIVEL BAJO: nivel entre 20% y 40%
        elif nivel < 40:
            if not alerta_activa('LOW'):
                Alert.objects.create(
                    tank=tank,
                    alert_type='LOW',
                    message=f'🟡 Tanque "{tank.name}" con nivel bajo: {nivel:.1f}%',
                    is_read=False
                )

        # Si el nivel vuelve a la normalidad (mayor a 40%), marcar alertas anteriores como leídas
        else:
            Alert.objects.filter(
                tank=tank,
                is_read=False
            ).update(is_read=True)