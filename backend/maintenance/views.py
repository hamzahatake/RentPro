from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Priority, MaintenanceStatus, MaintenanceRequest, MaintenanceRequestImage
from .serializers import PrioritySerializer, MaintenanceStatusSerializer, MaintenanceRequestSerializer, MaintenanceRequestImageSerializer

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['level', 'name', 'created_at']

class MaintenanceStatusViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceStatus.objects.filter(is_active=True)
    serializer_class = MaintenanceStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tenant__first_name', 'tenant__last_name', 'unit__unit_number']
    ordering_fields = ['requested_date', 'completed_date', 'created_at', 'cost']
    
    def get_queryset(self):
        queryset = MaintenanceRequest.objects.all()
        tenant = self.request.query_params.get('tenant', None)
        unit = self.request.query_params.get('unit', None)
        priority = self.request.query_params.get('priority', None)
        status = self.request.query_params.get('status', None)
        assigned_to = self.request.query_params.get('assigned_to', None)
        
        if tenant:
            queryset = queryset.filter(tenant_id=tenant)
        if unit:
            queryset = queryset.filter(unit_id=unit)
        if priority:
            queryset = queryset.filter(priority_id=priority)
        if status:
            queryset = queryset.filter(status_id=status)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        return queryset

class MaintenanceRequestImageViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequestImage.objects.all()
    serializer_class = MaintenanceRequestImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']
    
    def get_queryset(self):
        queryset = MaintenanceRequestImage.objects.all()
        maintenance_request = self.request.query_params.get('maintenance_request', None)
        
        if maintenance_request:
            queryset = queryset.filter(maintenance_request_id=maintenance_request)
        
        return queryset

