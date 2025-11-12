from rest_framework import serializers
from .models import PaymentMethod, PaymentStatus, Payment, PaymentHistory, RentSchedule
from leases.serializers import LeaseSerializer
from tenants.serializers import TenantSerializer
from users.serializers import UserSerializer

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = ['id', 'name', 'description', 'color_code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)
    lease_id = serializers.IntegerField(write_only=True)
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.IntegerField(write_only=True)
    payment_status = PaymentStatusSerializer(read_only=True)
    payment_status_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'lease', 'lease_id', 'tenant', 'tenant_id', 'amount', 'payment_date', 'due_date', 'payment_method', 'payment_method_id', 'payment_status', 'payment_status_id', 'transaction_id', 'receipt_number', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PaymentHistorySerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.IntegerField(write_only=True)
    status_before = PaymentStatusSerializer(read_only=True)
    status_before_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    status_after = PaymentStatusSerializer(read_only=True)
    status_after_id = serializers.IntegerField(write_only=True)
    changed_by = UserSerializer(read_only=True)
    changed_by_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PaymentHistory
        fields = ['id', 'payment', 'payment_id', 'status_before', 'status_before_id', 'status_after', 'status_after_id', 'changed_by', 'changed_by_id', 'changed_at', 'notes']
        read_only_fields = ['changed_at']

class RentScheduleSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)
    lease_id = serializers.IntegerField(write_only=True)
    status = PaymentStatusSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RentSchedule
        fields = ['id', 'lease', 'lease_id', 'due_date', 'amount', 'status', 'status_id', 'auto_generated', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

