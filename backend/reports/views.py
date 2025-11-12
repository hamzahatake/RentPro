from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ReportType, Report, AnalyticsSnapshot
from .serializers import ReportTypeSerializer, ReportSerializer, AnalyticsSnapshotSerializer

class ReportTypeViewSet(viewsets.ModelViewSet):
    queryset = ReportType.objects.filter(is_active=True)
    serializer_class = ReportTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['generated_at', 'title']
    
    def get_queryset(self):
        queryset = Report.objects.all()
        report_type = self.request.query_params.get('report_type', None)
        generated_by = self.request.query_params.get('generated_by', None)
        is_archived = self.request.query_params.get('is_archived', None)
        
        if report_type:
            queryset = queryset.filter(report_type_id=report_type)
        if generated_by:
            queryset = queryset.filter(generated_by_id=generated_by)
        if is_archived is not None:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

class AnalyticsSnapshotViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsSnapshot.objects.all()
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['snapshot_date']
    
    def get_queryset(self):
        queryset = AnalyticsSnapshot.objects.all()
        snapshot_date = self.request.query_params.get('snapshot_date', None)
        
        if snapshot_date:
            queryset = queryset.filter(snapshot_date=snapshot_date)
        
        return queryset

