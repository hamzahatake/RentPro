from rest_framework import serializers
from .models import LeaseType, LeaseStatus, RenewalStatus, Lease, LeaseRenewal
from tenants.serializers import TenantSerializer
from properties.serializers import UnitSerializer

class LeaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseType
        fields = ['id', 'name', 'description', 'default_duration_days', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LeaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseStatus
        fields = ['id', 'name', 'description', 'color_code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class RenewalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenewalStatus
        fields = ['id', 'name', 'description', 'color_code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LeaseSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.IntegerField(write_only=True)
    lease_type = LeaseTypeSerializer(read_only=True)
    lease_type_id = serializers.IntegerField(write_only=True)
    status = LeaseStatusSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Lease
        fields = ['id', 'tenant', 'tenant_id', 'unit', 'unit_id', 'lease_number', 'start_date', 'end_date', 'monthly_rent', 'deposit_amount', 'lease_type', 'lease_type_id', 'renewal_date', 'status', 'status_id', 'auto_renewal', 'terms_and_conditions', 'signed_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LeaseRenewalSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)
    lease_id = serializers.IntegerField(write_only=True)
    status = RenewalStatusSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = LeaseRenewal
        fields = ['id', 'lease', 'lease_id', 'renewal_date', 'new_end_date', 'new_monthly_rent', 'status', 'status_id', 'notes', 'created_at']
        read_only_fields = ['created_at']

