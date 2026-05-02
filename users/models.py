from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    roles = models.ManyToManyField(Rol, related_name='usuarios')
    
    def __str__(self):
        return f"{self.username} - {self.nombre} {self.apellido}"


class Recurso(models.Model):
    nombre = models.CharField(max_length=45)
    url_backend = models.CharField(max_length=100, blank=True, null=True)
    url_frontend = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    icono = models.CharField(max_length=45, blank=True, null=True)
    orden = models.IntegerField(default=0)
    recurso_padre = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='hijos')
    estado = models.BooleanField(default=True)
    roles = models.ManyToManyField(Rol, related_name='recursos')
    
    def __str__(self):
        return self.nombre