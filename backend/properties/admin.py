from django.contrib import admin
from .models import BuildingType, Building, UnitType, UnitStatus, Amenity, Unit, UnitImage

@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'building_type', 'owner', 'total_units', 'year_built', 'is_active', 'created_at']
    list_filter = ['building_type', 'is_active', 'year_built']
    search_fields = ['name', 'address__street_address', 'address__city', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['address', 'owner']

@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'bedrooms', 'bathrooms', 'is_active', 'created_at']
    list_filter = ['is_active', 'bedrooms']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UnitStatus)
class UnitStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit_number', 'building', 'unit_type', 'status', 'monthly_rent', 'bedrooms', 'bathrooms', 'created_at']
    list_filter = ['unit_type', 'status', 'bedrooms', 'bathrooms', 'building']
    search_fields = ['unit_number', 'building__name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['amenities']
    inlines = [UnitImageInline]
    raw_id_fields = ['building', 'unit_type', 'status']

@admin.register(UnitImage)
class UnitImageAdmin(admin.ModelAdmin):
    list_display = ['unit', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['unit__unit_number', 'unit__building__name']
    readonly_fields = ['uploaded_at']

