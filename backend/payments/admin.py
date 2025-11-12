from django.contrib import admin
from .models import PaymentMethod, PaymentStatus, Payment, PaymentHistory, RentSchedule

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    readonly_fields = ['changed_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'tenant', 'lease', 'amount', 'payment_date', 'due_date', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'payment_date', 'due_date']
    search_fields = ['receipt_number', 'transaction_id', 'tenant__first_name', 'tenant__last_name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['lease', 'tenant']
    inlines = [PaymentHistoryInline]

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['payment', 'status_before', 'status_after', 'changed_by', 'changed_at']
    list_filter = ['status_after', 'changed_at']
    search_fields = ['payment__receipt_number', 'payment__tenant__first_name']
    readonly_fields = ['changed_at']
    raw_id_fields = ['payment', 'changed_by']

@admin.register(RentSchedule)
class RentScheduleAdmin(admin.ModelAdmin):
    list_display = ['lease', 'due_date', 'amount', 'status', 'auto_generated', 'created_at']
    list_filter = ['status', 'auto_generated', 'due_date']
    search_fields = ['lease__lease_number', 'lease__tenant__first_name', 'lease__tenant__last_name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['lease']

