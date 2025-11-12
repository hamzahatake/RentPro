from rest_framework import serializers
from .models import IDProofType, Tenant, TenantUnitAssignment
from users.serializers import AddressSerializer, EmergencyContactSerializer
from properties.serializers import UnitSerializer

class IDProofTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDProofType
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TenantSerializer(serializers.ModelSerializer):
    emergency_contact = EmergencyContactSerializer(read_only=True)
    emergency_contact_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    mailing_address = AddressSerializer(read_only=True)
    mailing_address_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    id_proof_type = IDProofTypeSerializer(read_only=True)
    id_proof_type_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Tenant
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'alternate_phone', 'date_of_birth', 'emergency_contact', 'emergency_contact_id', 'mailing_address', 'mailing_address_id', 'id_proof_type', 'id_proof_type_id', 'id_proof_number', 'notes', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TenantUnitAssignmentSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TenantUnitAssignment
        fields = ['id', 'tenant', 'tenant_id', 'unit', 'unit_id', 'assigned_date', 'vacated_date', 'is_current', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

