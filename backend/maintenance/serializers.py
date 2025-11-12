from rest_framework import serializers
from .models import Priority, MaintenanceStatus, MaintenanceRequest, MaintenanceRequestImage
from tenants.serializers import TenantSerializer
from properties.serializers import UnitSerializer
from users.serializers import UserSerializer

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name', 'level', 'color_code', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MaintenanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceStatus
        fields = ['id', 'name', 'description', 'color_code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MaintenanceRequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequestImage
        fields = ['id', 'maintenance_request', 'image', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.IntegerField(write_only=True)
    priority = PrioritySerializer(read_only=True)
    priority_id = serializers.IntegerField(write_only=True)
    status = MaintenanceStatusSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    images = MaintenanceRequestImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'tenant', 'tenant_id', 'unit', 'unit_id', 'title', 'description', 'priority', 'priority_id', 'status', 'status_id', 'requested_date', 'completed_date', 'assigned_to', 'assigned_to_id', 'cost', 'notes', 'images', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

