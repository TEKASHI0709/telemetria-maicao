from django.contrib import admin
from .models import SystemLog


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('log_type', 'level', 'message', 'user', 'created_at')
    list_filter = ('level', 'log_type', 'created_at')
    search_fields = ('message', 'user__username')
    readonly_fields = ('log_type', 'level', 'message', 'user', 'metadata', 'created_at')
    date_hierarchy = 'created_at'