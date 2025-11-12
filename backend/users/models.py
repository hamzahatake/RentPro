from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator, RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('landlord', 'Landlord'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
    ]
    
    phone_number = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='manager')
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def is_landlord(self):
        return self.role == 'landlord'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_accountant(self):
        return self.role == 'accountant'
    
    def __str__(self):
        return self.get_full_name() or self.username

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('building', 'Building'),
        ('tenant', 'Tenant'),
        ('mailing', 'Mailing'),
        ('other', 'Other'),
    ]
    
    street_address = models.CharField(max_length=255)
    street_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'addresses'
        indexes = [
            models.Index(fields=['address_type']),
            models.Index(fields=['city']),
            models.Index(fields=['state']),
        ]
    
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.zip_code}"

class EmergencyContact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ]
    
    contact_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='other')
    phone_number = models.CharField(max_length=20, validators=[phone_validator])
    alternate_phone = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True)
    email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'emergency_contacts'
    
    def __str__(self):
        return f"{self.contact_name} ({self.relationship})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    emergency_contact = models.ForeignKey('EmergencyContact', on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile for {self.user.get_full_name()}"

