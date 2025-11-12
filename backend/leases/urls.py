from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaseTypeViewSet, LeaseStatusViewSet, RenewalStatusViewSet, LeaseViewSet, LeaseRenewalViewSet

router = DefaultRouter()
router.register(r'lease-types', LeaseTypeViewSet, basename='lease-type')
router.register(r'lease-statuses', LeaseStatusViewSet, basename='lease-status')
router.register(r'renewal-statuses', RenewalStatusViewSet, basename='renewal-status')
router.register(r'leases', LeaseViewSet, basename='lease')
router.register(r'renewals', LeaseRenewalViewSet, basename='lease-renewal')

urlpatterns = [
    path('', include(router.urls)),
]

