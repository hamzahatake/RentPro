from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import NotificationType, ReminderType, DeliveryMethod, Notification, Reminder, ReminderLog
from .serializers import NotificationTypeSerializer, ReminderTypeSerializer, DeliveryMethodSerializer, NotificationSerializer, ReminderSerializer, ReminderLogSerializer

class NotificationTypeViewSet(viewsets.ModelViewSet):
    queryset = NotificationType.objects.filter(is_active=True)
    serializer_class = NotificationTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ReminderTypeViewSet(viewsets.ModelViewSet):
    queryset = ReminderType.objects.filter(is_active=True)
    serializer_class = ReminderTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class DeliveryMethodViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMethod.objects.filter(is_active=True)
    serializer_class = DeliveryMethodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'is_read']
    
    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        is_read = self.request.query_params.get('is_read', None)
        notification_type = self.request.query_params.get('notification_type', None)
        
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        if notification_type:
            queryset = queryset.filter(notification_type_id=notification_type)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True, read_at=timezone.now())
        return Response({'status': 'all marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count})

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        queryset = Reminder.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class ReminderLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReminderLog.objects.all()
    serializer_class = ReminderLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    
    def get_queryset(self):
        queryset = ReminderLog.objects.all()
        reminder = self.request.query_params.get('reminder', None)
        sent_to = self.request.query_params.get('sent_to', None)
        status = self.request.query_params.get('status', None)
        
        if reminder:
            queryset = queryset.filter(reminder_id=reminder)
        if sent_to:
            queryset = queryset.filter(sent_to_id=sent_to)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

