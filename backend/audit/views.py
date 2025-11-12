from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['model_name', 'object_id', 'action']
    ordering_fields = ['timestamp']
    
    def get_queryset(self):
        queryset = AuditLog.objects.all()
        user = self.request.query_params.get('user', None)
        action = self.request.query_params.get('action', None)
        model_name = self.request.query_params.get('model_name', None)
        
        if user:
            queryset = queryset.filter(user_id=user)
        if action:
            queryset = queryset.filter(action=action)
        if model_name:
            queryset = queryset.filter(model_name=model_name)
        
        return queryset

