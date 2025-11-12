from rest_framework import serializers
from .models import NotificationType, ReminderType, DeliveryMethod, Notification, Reminder, ReminderLog
from leases.serializers import LeaseSerializer
from payments.serializers import PaymentSerializer
from maintenance.serializers import MaintenanceRequestSerializer
from users.serializers import UserSerializer

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['id', 'name', 'description', 'icon', 'default_template', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReminderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderType
        fields = ['id', 'name', 'description', 'default_days_before', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.IntegerField(write_only=True)
    notification_type = NotificationTypeSerializer(read_only=True)
    notification_type_id = serializers.IntegerField(write_only=True)
    related_lease = LeaseSerializer(read_only=True)
    related_lease_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    related_payment = PaymentSerializer(read_only=True)
    related_payment_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    related_maintenance_request = MaintenanceRequestSerializer(read_only=True)
    related_maintenance_request_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_id', 'notification_type', 'notification_type_id', 'title', 'message', 'is_read', 'read_at', 'created_at', 'related_lease', 'related_lease_id', 'related_payment', 'related_payment_id', 'related_maintenance_request', 'related_maintenance_request_id']
        read_only_fields = ['read_at', 'created_at']

class ReminderSerializer(serializers.ModelSerializer):
    reminder_type = ReminderTypeSerializer(read_only=True)
    reminder_type_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Reminder
        fields = ['id', 'reminder_type', 'reminder_type_id', 'days_before', 'is_active', 'email_enabled', 'sms_enabled', 'message_template', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReminderLogSerializer(serializers.ModelSerializer):
    reminder = ReminderSerializer(read_only=True)
    reminder_id = serializers.IntegerField(write_only=True)
    sent_to = UserSerializer(read_only=True)
    sent_to_id = serializers.IntegerField(write_only=True)
    delivery_method = DeliveryMethodSerializer(read_only=True)
    delivery_method_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ReminderLog
        fields = ['id', 'reminder', 'reminder_id', 'sent_to', 'sent_to_id', 'sent_at', 'delivery_method', 'delivery_method_id', 'status', 'error_message']
        read_only_fields = ['sent_at']

