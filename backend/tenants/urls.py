from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IDProofTypeViewSet, TenantViewSet, TenantUnitAssignmentViewSet

router = DefaultRouter()
router.register(r'id-proof-types', IDProofTypeViewSet, basename='id-proof-type')
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'assignments', TenantUnitAssignmentViewSet, basename='tenant-unit-assignment')

urlpatterns = [
    path('', include(router.urls)),
]

