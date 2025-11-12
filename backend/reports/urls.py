from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportTypeViewSet, ReportViewSet, AnalyticsSnapshotViewSet

router = DefaultRouter()
router.register(r'report-types', ReportTypeViewSet, basename='report-type')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'analytics', AnalyticsSnapshotViewSet, basename='analytics-snapshot')

urlpatterns = [
    path('', include(router.urls)),
]

