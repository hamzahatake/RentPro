from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentStatusViewSet, PaymentViewSet, PaymentHistoryViewSet, RentScheduleViewSet

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')
router.register(r'payment-statuses', PaymentStatusViewSet, basename='payment-status')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payment-history', PaymentHistoryViewSet, basename='payment-history')
router.register(r'rent-schedules', RentScheduleViewSet, basename='rent-schedule')

urlpatterns = [
    path('', include(router.urls)),
]

