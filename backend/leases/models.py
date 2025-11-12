from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from users.models import User
from tenants.models import Tenant
from properties.models import Unit

class LeaseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    default_duration_days = models.PositiveIntegerField(default=365)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lease_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class LeaseStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lease_statuses'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class RenewalStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'renewal_statuses'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='leases')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='leases')
    lease_number = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    lease_type = models.ForeignKey(LeaseType, on_delete=models.PROTECT, related_name='leases')
    renewal_date = models.DateField(blank=True, null=True)
    status = models.ForeignKey(LeaseStatus, on_delete=models.PROTECT, related_name='leases')
    auto_renewal = models.BooleanField(default=False)
    terms_and_conditions = models.TextField(blank=True, null=True)
    signed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leases'
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['unit']),
            models.Index(fields=['lease_type']),
            models.Index(fields=['status']),
            models.Index(fields=['end_date']),
            models.Index(fields=['start_date']),
        ]
        ordering = ['-start_date']
    
    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after start date.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Lease {self.lease_number} - {self.tenant} - {self.unit}"

class LeaseRenewal(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='renewals')
    renewal_date = models.DateField()
    new_end_date = models.DateField()
    new_monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.ForeignKey(RenewalStatus, on_delete=models.PROTECT, related_name='renewals')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lease_renewals'
        indexes = [
            models.Index(fields=['lease']),
            models.Index(fields=['status']),
            models.Index(fields=['renewal_date']),
        ]
        ordering = ['-renewal_date']
    
    def clean(self):
        if self.renewal_date and self.new_end_date:
            if self.new_end_date <= self.renewal_date:
                raise ValidationError("New end date must be after renewal date.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Renewal for {self.lease} - {self.status}"

