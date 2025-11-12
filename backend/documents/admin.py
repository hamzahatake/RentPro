from django.contrib import admin
from .models import DocumentType, Tag, Document

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'document_type', 'uploaded_by', 'related_lease', 'related_tenant', 'related_unit', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['name', 'description', 'uploaded_by__username']
    readonly_fields = ['file_size', 'mime_type', 'uploaded_at']
    filter_horizontal = ['tags']
    raw_id_fields = ['related_lease', 'related_tenant', 'related_unit', 'related_maintenance_request', 'uploaded_by']

