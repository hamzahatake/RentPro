from rest_framework import serializers
from .models import ReportType, Report, AnalyticsSnapshot
from users.serializers import UserSerializer

class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'description', 'default_template', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReportSerializer(serializers.ModelSerializer):
    report_type = ReportTypeSerializer(read_only=True)
    report_type_id = serializers.IntegerField(write_only=True)
    generated_by = UserSerializer(read_only=True)
    generated_by_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'report_type_id', 'title', 'generated_by', 'generated_by_id', 'generated_at', 'date_range_start', 'date_range_end', 'file_path', 'parameters', 'is_archived']
        read_only_fields = ['generated_at']
    
    def create(self, validated_data):
        generated_by_id = validated_data.pop('generated_by_id', None)
        report = Report.objects.create(**validated_data)
        if generated_by_id:
            report.generated_by_id = generated_by_id
        else:
            report.generated_by = self.context['request'].user
        report.save()
        return report

class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshot
        fields = ['id', 'snapshot_date', 'total_units', 'occupied_units', 'vacant_units', 'total_monthly_rent', 'collected_rent', 'pending_rent', 'overdue_amount', 'occupancy_rate', 'average_rent', 'data']
        read_only_fields = []

