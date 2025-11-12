from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import IDProofType, Tenant, TenantUnitAssignment
from .serializers import IDProofTypeSerializer, TenantSerializer, TenantUnitAssignmentSerializer

class IDProofTypeViewSet(viewsets.ModelViewSet):
    queryset = IDProofType.objects.filter(is_active=True)
    serializer_class = IDProofTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'id_proof_number']
    ordering_fields = ['first_name', 'last_name', 'email', 'created_at']
    
    def get_queryset(self):
        queryset = Tenant.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class TenantUnitAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TenantUnitAssignment.objects.all()
    serializer_class = TenantUnitAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['assigned_date', 'created_at']
    
    def get_queryset(self):
        queryset = TenantUnitAssignment.objects.all()
        tenant = self.request.query_params.get('tenant', None)
        unit = self.request.query_params.get('unit', None)
        is_current = self.request.query_params.get('is_current', None)
        
        if tenant:
            queryset = queryset.filter(tenant_id=tenant)
        if unit:
            queryset = queryset.filter(unit_id=unit)
        if is_current is not None:
            queryset = queryset.filter(is_current=is_current.lower() == 'true')
        
        return queryset

