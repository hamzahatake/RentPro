from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from tenants.models import Tenant
from leases.models import Lease

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_methods'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class PaymentStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_statuses'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.PROTECT, related_name='payments')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    due_date = models.DateField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='payments')
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, related_name='payments')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['lease']),
            models.Index(fields=['tenant']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['payment_date']),
        ]
        ordering = ['-payment_date', '-due_date']
    
    def __str__(self):
        return f"Payment {self.receipt_number or self.id} - {self.tenant} - ${self.amount}"

class PaymentHistory(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='history')
    status_before = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, blank=True, null=True, related_name='payment_histories_before')
    status_after = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, related_name='payment_histories_after')
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_history_changes')
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'payment_history'
        indexes = [
            models.Index(fields=['payment']),
            models.Index(fields=['changed_at']),
        ]
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"Payment {self.payment.id} - {self.status_before} -> {self.status_after}"


class RentSchedule(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='rent_schedules')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, related_name='rent_schedules')
    auto_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rent_schedules'
        indexes = [
            models.Index(fields=['lease']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
        ]
        ordering = ['due_date']
    
    def __str__(self):
        return f"Rent Schedule - {self.lease} - ${self.amount} due {self.due_date}"

