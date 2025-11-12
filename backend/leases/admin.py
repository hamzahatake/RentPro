from django.contrib import admin
from .models import LeaseType, LeaseStatus, RenewalStatus, Lease, LeaseRenewal

@admin.register(LeaseType)
class LeaseTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_duration_days', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LeaseStatus)
class LeaseStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RenewalStatus)
class RenewalStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

class LeaseRenewalInline(admin.TabularInline):
    model = LeaseRenewal
    extra = 0

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['lease_number', 'tenant', 'unit', 'start_date', 'end_date', 'monthly_rent', 'lease_type', 'status', 'auto_renewal', 'created_at']
    list_filter = ['lease_type', 'status', 'auto_renewal', 'start_date', 'end_date']
    search_fields = ['lease_number', 'tenant__first_name', 'tenant__last_name', 'unit__unit_number']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['tenant', 'unit']
    inlines = [LeaseRenewalInline]

@admin.register(LeaseRenewal)
class LeaseRenewalAdmin(admin.ModelAdmin):
    list_display = ['lease', 'renewal_date', 'new_end_date', 'new_monthly_rent', 'status', 'created_at']
    list_filter = ['status', 'renewal_date']
    search_fields = ['lease__lease_number', 'lease__tenant__first_name', 'lease__tenant__last_name']
    readonly_fields = ['created_at']
    raw_id_fields = ['lease']

