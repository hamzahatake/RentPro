from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from tenants.models import Tenant
from properties.models import Unit

class Priority(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(default=0)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'priorities'
        ordering = ['level']
        verbose_name_plural = 'Priorities'
    
    def __str__(self):
        return self.name

class MaintenanceStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maintenance_statuses'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='maintenance_requests')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='maintenance_requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='maintenance_requests')
    status = models.ForeignKey(MaintenanceStatus, on_delete=models.PROTECT, related_name='maintenance_requests')
    requested_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_maintenance_requests')
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maintenance_requests'
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['unit']),
            models.Index(fields=['priority']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
        ]
        ordering = ['-requested_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.unit} - {self.tenant}"

class MaintenanceRequestImage(models.Model):
    maintenance_request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='maintenance_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'maintenance_request_images'
        indexes = [
            models.Index(fields=['maintenance_request']),
        ]
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Image for {self.maintenance_request}"

