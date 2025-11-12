from django.contrib import admin
from .models import ReportType, Report, AnalyticsSnapshot

@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'generated_at', 'date_range_start', 'date_range_end', 'is_archived']
    list_filter = ['report_type', 'is_archived', 'generated_at']
    search_fields = ['title', 'generated_by__username']
    readonly_fields = ['generated_at']
    raw_id_fields = ['generated_by']

@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ['snapshot_date', 'total_units', 'occupied_units', 'vacant_units', 'occupancy_rate', 'total_monthly_rent', 'collected_rent']
    list_filter = ['snapshot_date']
    search_fields = ['snapshot_date']
    readonly_fields = []

