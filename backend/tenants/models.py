from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from users.models import Address, EmergencyContact

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class IDProofType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'id_proof_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=20, validators=[phone_validator])
    alternate_phone = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.SET_NULL, blank=True, null=True, related_name='tenants')
    mailing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='tenants')
    id_proof_type = models.ForeignKey(IDProofType, on_delete=models.SET_NULL, blank=True, null=True, related_name='tenants')
    id_proof_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tenants'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['id_proof_type']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['last_name', 'first_name']
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_full_name()

class TenantUnitAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='unit_assignments')
    unit = models.ForeignKey('properties.Unit', on_delete=models.CASCADE, related_name='tenant_assignments')
    assigned_date = models.DateField()
    vacated_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tenant_unit_assignments'
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['unit']),
            models.Index(fields=['is_current']),
        ]
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.tenant} - {self.unit}"

