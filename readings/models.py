from django.db import models
from tanks.models import Tank

class Reading(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, related_name='readings')
    distance_cm = models.FloatField()
    level_percent = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tank.name} - {self.level_percent}% - {self.timestamp}"