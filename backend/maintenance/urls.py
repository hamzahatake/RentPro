from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriorityViewSet, MaintenanceStatusViewSet, MaintenanceRequestViewSet, MaintenanceRequestImageViewSet

router = DefaultRouter()
router.register(r'priorities', PriorityViewSet, basename='priority')
router.register(r'maintenance-statuses', MaintenanceStatusViewSet, basename='maintenance-status')
router.register(r'requests', MaintenanceRequestViewSet, basename='maintenance-request')
router.register(r'request-images', MaintenanceRequestImageViewSet, basename='maintenance-request-image')

urlpatterns = [
    path('', include(router.urls)),
]

