from rest_framework import serializers
from .models import DocumentType, Tag, Document
from leases.serializers import LeaseSerializer
from tenants.serializers import TenantSerializer
from properties.serializers import UnitSerializer
from maintenance.serializers import MaintenanceRequestSerializer
from users.serializers import UserSerializer

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color_code', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.IntegerField(write_only=True)
    related_lease = LeaseSerializer(read_only=True)
    related_lease_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    related_tenant = TenantSerializer(read_only=True)
    related_tenant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    related_unit = UnitSerializer(read_only=True)
    related_unit_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    related_maintenance_request = MaintenanceRequestSerializer(read_only=True)
    related_maintenance_request_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), write_only=True, required=False)
    
    class Meta:
        model = Document
        fields = ['id', 'name', 'document_type', 'document_type_id', 'file', 'file_size', 'mime_type', 'related_lease', 'related_lease_id', 'related_tenant', 'related_tenant_id', 'related_unit', 'related_unit_id', 'related_maintenance_request', 'related_maintenance_request_id', 'uploaded_by', 'uploaded_by_id', 'uploaded_at', 'description', 'tags', 'tag_ids']
        read_only_fields = ['file_size', 'mime_type', 'uploaded_by', 'uploaded_at']
    
    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        uploaded_by_id = validated_data.pop('uploaded_by_id', None)
        document = Document.objects.create(**validated_data)
        if uploaded_by_id:
            document.uploaded_by_id = uploaded_by_id
        else:
            document.uploaded_by = self.context['request'].user
        document.save()
        if tag_ids:
            document.tags.set(tag_ids)
        return document
    
    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance

