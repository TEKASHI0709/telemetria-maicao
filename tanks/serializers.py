from rest_framework import serializers
from .models import Tank


class TankSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Tank
        fields = ['id', 'name', 'location', 'capacity_liters', 'height_cm', 'created_at', 'owner', 'owner_username']
        read_only_fields = ['owner', 'created_at']