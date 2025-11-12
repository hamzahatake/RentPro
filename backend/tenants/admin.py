from django.contrib import admin
from .models import IDProofType, Tenant, TenantUnitAssignment

@admin.register(IDProofType)
class IDProofTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'id_proof_type', 'is_active', 'created_at']
    list_filter = ['id_proof_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'id_proof_number']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['emergency_contact', 'mailing_address']

@admin.register(TenantUnitAssignment)
class TenantUnitAssignmentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'unit', 'assigned_date', 'vacated_date', 'is_current', 'created_at']
    list_filter = ['is_current', 'assigned_date']
    search_fields = ['tenant__first_name', 'tenant__last_name', 'unit__unit_number', 'unit__building__name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['tenant', 'unit']

