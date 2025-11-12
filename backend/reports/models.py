from django.db import models
from django.core.validators import MinValueValidator
from users.models import User

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

class ReportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    default_template = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Report(models.Model):
    report_type = models.ForeignKey(ReportType, on_delete=models.PROTECT, related_name='reports')
    title = models.CharField(max_length=255)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    date_range_start = models.DateField(blank=True, null=True)
    date_range_end = models.DateField(blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    parameters = JSONField(default=dict, blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['report_type']),
            models.Index(fields=['generated_by']),
            models.Index(fields=['generated_at']),
            models.Index(fields=['is_archived']),
        ]
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.report_type}"

class AnalyticsSnapshot(models.Model):
    snapshot_date = models.DateField(unique=True)
    total_units = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    occupied_units = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    vacant_units = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    total_monthly_rent = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    collected_rent = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    pending_rent = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    overdue_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    average_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    data = JSONField(default=dict, blank=True, null=True)
    
    class Meta:
        db_table = 'analytics_snapshots'
        indexes = [
            models.Index(fields=['snapshot_date']),
        ]
        ordering = ['-snapshot_date']
    
    def __str__(self):
        return f"Analytics Snapshot - {self.snapshot_date}"

