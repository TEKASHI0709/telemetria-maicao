from rest_framework import serializers
from .models import SystemLog


class SystemLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True, default=None)
    log_type_display = serializers.CharField(source='get_log_type_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = SystemLog
        fields = [
            'id', 'log_type', 'log_type_display', 'level', 'level_display',
            'message', 'user', 'user_username', 'metadata', 'created_at'
        ]
        read_only_fields = ['created_at']