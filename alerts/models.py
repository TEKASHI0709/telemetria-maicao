from django.db import models
from tanks.models import Tank

class Alert(models.Model):
    LEVEL_CHOICES = [
        ('LOW', 'Nivel bajo'),
        ('CRITICAL', 'Nivel crítico'),
        ('OVERFLOW', 'Desbordamiento'),
    ]

    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} - {self.tank.name} - {self.created_at}"