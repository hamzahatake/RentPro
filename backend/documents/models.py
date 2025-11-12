from django.db import models
from users.models import User
from tenants.models import Tenant
from properties.models import Unit
from leases.models import Lease
from maintenance.models import MaintenanceRequest

class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'document_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=255)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name='documents')
    file = models.FileField(upload_to='documents/')
    file_size = models.PositiveIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    related_lease = models.ForeignKey(Lease, on_delete=models.SET_NULL, blank=True, null=True, related_name='documents')
    related_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True, related_name='documents')
    related_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True, related_name='documents')
    related_maintenance_request = models.ForeignKey(MaintenanceRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='documents')
    
    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['document_type']),
            models.Index(fields=['related_lease']),
            models.Index(fields=['related_tenant']),
            models.Index(fields=['related_unit']),
            models.Index(fields=['uploaded_by']),
        ]
        ordering = ['-uploaded_at']
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.mime_type = self.file.content_type
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

