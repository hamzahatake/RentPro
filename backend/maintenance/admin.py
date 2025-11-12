from django.contrib import admin
from .models import Priority, MaintenanceStatus, MaintenanceRequest, MaintenanceRequestImage

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'color_code', 'created_at']
    list_filter = ['level']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MaintenanceStatus)
class MaintenanceStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

class MaintenanceRequestImageInline(admin.TabularInline):
    model = MaintenanceRequestImage
    extra = 1

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'tenant', 'unit', 'priority', 'status', 'assigned_to', 'requested_date', 'completed_date', 'cost', 'created_at']
    list_filter = ['priority', 'status', 'assigned_to', 'requested_date', 'completed_date']
    search_fields = ['title', 'description', 'tenant__first_name', 'tenant__last_name', 'unit__unit_number']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['tenant', 'unit', 'assigned_to']
    inlines = [MaintenanceRequestImageInline]

@admin.register(MaintenanceRequestImage)
class MaintenanceRequestImageAdmin(admin.ModelAdmin):
    list_display = ['maintenance_request', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['maintenance_request__title']
    readonly_fields = ['uploaded_at']
    raw_id_fields = ['maintenance_request']

