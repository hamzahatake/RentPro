from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Address, EmergencyContact, UserProfile

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street_address', 'street_address_line2', 'city', 'state', 'zip_code', 'country', 'address_type', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class EmergencyContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = EmergencyContact
        fields = ['id', 'contact_name', 'relationship', 'phone_number', 'alternate_phone', 'email', 'address', 'address_id', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        address_id = validated_data.pop('address_id', None)
        if address_id:
            validated_data['address_id'] = address_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        address_id = validated_data.pop('address_id', None)
        if address_id is not None:
            validated_data['address_id'] = address_id
        return super().update(instance, validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    emergency_contact = EmergencyContactSerializer(read_only=True)
    address_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    emergency_contact_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'profile_picture', 'address', 'address_id', 'emergency_contact', 'emergency_contact_id', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'is_active', 'date_joined', 'password', 'profile']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

