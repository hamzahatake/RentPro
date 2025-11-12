from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import DocumentType, Tag, Document
from .serializers import DocumentTypeSerializer, TagSerializer, DocumentSerializer

class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.filter(is_active=True)
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    
    def get_queryset(self):
        queryset = Document.objects.all()
        document_type = self.request.query_params.get('document_type', None)
        related_lease = self.request.query_params.get('related_lease', None)
        related_tenant = self.request.query_params.get('related_tenant', None)
        related_unit = self.request.query_params.get('related_unit', None)
        uploaded_by = self.request.query_params.get('uploaded_by', None)
        
        if document_type:
            queryset = queryset.filter(document_type_id=document_type)
        if related_lease:
            queryset = queryset.filter(related_lease_id=related_lease)
        if related_tenant:
            queryset = queryset.filter(related_tenant_id=related_tenant)
        if related_unit:
            queryset = queryset.filter(related_unit_id=related_unit)
        if uploaded_by:
            queryset = queryset.filter(uploaded_by_id=uploaded_by)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

