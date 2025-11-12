from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import LeaseType, LeaseStatus, RenewalStatus, Lease, LeaseRenewal
from .serializers import LeaseTypeSerializer, LeaseStatusSerializer, RenewalStatusSerializer, LeaseSerializer, LeaseRenewalSerializer

class LeaseTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaseType.objects.filter(is_active=True)
    serializer_class = LeaseTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class LeaseStatusViewSet(viewsets.ModelViewSet):
    queryset = LeaseStatus.objects.filter(is_active=True)
    serializer_class = LeaseStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class RenewalStatusViewSet(viewsets.ModelViewSet):
    queryset = RenewalStatus.objects.filter(is_active=True)
    serializer_class = RenewalStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['lease_number', 'tenant__first_name', 'tenant__last_name', 'unit__unit_number']
    ordering_fields = ['start_date', 'end_date', 'created_at', 'lease_number']
    
    def get_queryset(self):
        queryset = Lease.objects.all()
        tenant = self.request.query_params.get('tenant', None)
        unit = self.request.query_params.get('unit', None)
        lease_type = self.request.query_params.get('lease_type', None)
        status = self.request.query_params.get('status', None)
        
        if tenant:
            queryset = queryset.filter(tenant_id=tenant)
        if unit:
            queryset = queryset.filter(unit_id=unit)
        if lease_type:
            queryset = queryset.filter(lease_type_id=lease_type)
        if status:
            queryset = queryset.filter(status_id=status)
        
        return queryset

class LeaseRenewalViewSet(viewsets.ModelViewSet):
    queryset = LeaseRenewal.objects.all()
    serializer_class = LeaseRenewalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['renewal_date', 'created_at']
    
    def get_queryset(self):
        queryset = LeaseRenewal.objects.all()
        lease = self.request.query_params.get('lease', None)
        status = self.request.query_params.get('status', None)
        
        if lease:
            queryset = queryset.filter(lease_id=lease)
        if status:
            queryset = queryset.filter(status_id=status)
        
        return queryset

