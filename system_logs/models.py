from django.db import models
from django.conf import settings


class SystemLog(models.Model):
    LOG_TYPES = [
        ('USER_CREATED', 'Usuario creado'),
        ('USER_UPDATED', 'Usuario actualizado'),
        ('USER_DELETED', 'Usuario eliminado'),
        ('TANK_CREATED', 'Tanque creado'),
        ('TANK_DELETED', 'Tanque eliminado'),
        ('DEVICE_ONLINE', 'Dispositivo conectado'),
        ('DEVICE_OFFLINE', 'Dispositivo desconectado'),
        ('LOGIN_SUCCESS', 'Inicio de sesión exitoso'),
        ('LOGIN_FAILED', 'Intento de sesión fallido'),
        ('SYSTEM', 'Evento del sistema'),
    ]

    LOG_LEVELS = [
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Éxito'),
    ]

    log_type = models.CharField(max_length=30, choices=LOG_TYPES)
    level = models.CharField(max_length=10, choices=LOG_LEVELS, default='INFO')
    message = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='system_logs'
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level}] {self.log_type} - {self.created_at}"