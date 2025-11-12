from rest_framework import serializers
from .models import BuildingType, Building, UnitType, UnitStatus, Amenity, Unit, UnitImage
from users.serializers import AddressSerializer

class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingType
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BuildingSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.IntegerField(write_only=True)
    building_type = BuildingTypeSerializer(read_only=True)
    building_type_id = serializers.IntegerField(write_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    
    class Meta:
        model = Building
        fields = ['id', 'name', 'address', 'address_id', 'building_type', 'building_type_id', 'total_units', 'year_built', 'owner', 'owner_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = ['id', 'name', 'bedrooms', 'bathrooms', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UnitStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitStatus
        fields = ['id', 'name', 'description', 'color_code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'icon', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ['id', 'unit', 'image', 'caption', 'is_primary', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class UnitSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)
    building_id = serializers.IntegerField(write_only=True)
    unit_type = UnitTypeSerializer(read_only=True)
    unit_type_id = serializers.IntegerField(write_only=True)
    status = UnitStatusSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Amenity.objects.all(), write_only=True, required=False)
    images = UnitImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ['id', 'building', 'building_id', 'unit_number', 'unit_type', 'unit_type_id', 'size', 'monthly_rent', 'deposit_amount', 'status', 'status_id', 'floor_number', 'bedrooms', 'bathrooms', 'amenities', 'amenity_ids', 'images', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        amenity_ids = validated_data.pop('amenity_ids', [])
        unit = Unit.objects.create(**validated_data)
        if amenity_ids:
            unit.amenities.set(amenity_ids)
        return unit
    
    def update(self, instance, validated_data):
        amenity_ids = validated_data.pop('amenity_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if amenity_ids is not None:
            instance.amenities.set(amenity_ids)
        return instance

