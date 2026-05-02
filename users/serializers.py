from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Rol, Recurso

Usuario = get_user_model()


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    roles = RolSerializer(many=True, read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'nombre', 'apellido', 'roles', 'is_active']