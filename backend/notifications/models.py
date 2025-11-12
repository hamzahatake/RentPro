from django.db import models
from users.models import User
from leases.models import Lease
from payments.models import Payment
from maintenance.models import MaintenanceRequest

class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    default_template = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ReminderType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    default_days_before = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reminder_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'delivery_methods'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.ForeignKey(NotificationType, on_delete=models.PROTECT, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_lease = models.ForeignKey(Lease, on_delete=models.SET_NULL, blank=True, null=True, related_name='notifications')
    related_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, related_name='notifications')
    related_maintenance_request = models.ForeignKey(MaintenanceRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='notifications')
    
    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient}"

class Reminder(models.Model):
    reminder_type = models.ForeignKey(ReminderType, on_delete=models.PROTECT, related_name='reminders')
    days_before = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    message_template = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reminders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reminder_type} - {self.days_before} days before"

class ReminderLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='logs')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminder_logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.PROTECT, related_name='reminder_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'reminder_logs'
        indexes = [
            models.Index(fields=['reminder']),
            models.Index(fields=['sent_to']),
            models.Index(fields=['delivery_method']),
            models.Index(fields=['status']),
            models.Index(fields=['sent_at']),
        ]
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.reminder} - {self.sent_to} - {self.status}"

