from django.db import models
from django.core.validators import MinValueValidator
from users.models import User, Address

class BuildingType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'building_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='buildings')
    building_type = models.ForeignKey(BuildingType, on_delete=models.PROTECT, related_name='buildings')
    total_units = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    year_built = models.PositiveIntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owned_buildings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'buildings'
        indexes = [
            models.Index(fields=['address']),
            models.Index(fields=['building_type']),
            models.Index(fields=['owner']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['name']
    
    def __str__(self):
        return self.name

class UnitType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unit_types'
        ordering = ['bedrooms', 'bathrooms']
    
    def __str__(self):
        return self.name

class UnitStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unit_statuses'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'amenities'
        ordering = ['name']
        verbose_name_plural = 'Amenities'
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50)
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT, related_name='units')
    size = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Size in square feet")
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    status = models.ForeignKey(UnitStatus, on_delete=models.PROTECT, related_name='units')
    floor_number = models.IntegerField(blank=True, null=True)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='units')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'units'
        unique_together = ['building', 'unit_number']
        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['unit_type']),
            models.Index(fields=['status']),
            models.Index(fields=['unit_number']),
        ]
        ordering = ['building', 'unit_number']
    
    def __str__(self):
        return f"{self.building.name} - Unit {self.unit_number}"

class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='unit_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'unit_images'
        indexes = [
            models.Index(fields=['unit']),
            models.Index(fields=['is_primary']),
        ]
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.unit}"

