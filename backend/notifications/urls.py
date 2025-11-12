from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationTypeViewSet, ReminderTypeViewSet, DeliveryMethodViewSet, NotificationViewSet, ReminderViewSet, ReminderLogViewSet

router = DefaultRouter()
router.register(r'notification-types', NotificationTypeViewSet, basename='notification-type')
router.register(r'reminder-types', ReminderTypeViewSet, basename='reminder-type')
router.register(r'delivery-methods', DeliveryMethodViewSet, basename='delivery-method')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'reminders', ReminderViewSet, basename='reminder')
router.register(r'reminder-logs', ReminderLogViewSet, basename='reminder-log')

urlpatterns = [
    path('', include(router.urls)),
]

