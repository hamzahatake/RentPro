from django.contrib import admin
from .models import NotificationType, ReminderType, DeliveryMethod, Notification, Reminder, ReminderLog

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ReminderType)
class ReminderTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_days_before', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'read_at', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'read_at']
    raw_id_fields = ['recipient', 'related_lease', 'related_payment', 'related_maintenance_request']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['reminder_type', 'days_before', 'is_active', 'email_enabled', 'sms_enabled', 'created_at']
    list_filter = ['is_active', 'email_enabled', 'sms_enabled']
    search_fields = ['reminder_type__name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['reminder_type']

@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ['reminder', 'sent_to', 'delivery_method', 'status', 'sent_at']
    list_filter = ['status', 'delivery_method', 'sent_at']
    search_fields = ['reminder__reminder_type__name', 'sent_to__username', 'sent_to__email']
    readonly_fields = ['sent_at']
    raw_id_fields = ['reminder', 'sent_to']

