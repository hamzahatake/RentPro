from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'model_name', 'object_id', 'user', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['model_name', 'object_id', 'user__username', 'user__email', 'ip_address']
    readonly_fields = ['timestamp']
    raw_id_fields = ['user']
    date_hierarchy = 'timestamp'

