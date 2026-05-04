from django.db import models
from django.conf import settings

class Tank(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tanks'
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity_liters = models.FloatField()
    height_cm = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location} ({self.owner.username})"