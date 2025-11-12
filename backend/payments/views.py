from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import PaymentMethod, PaymentStatus, Payment, PaymentHistory, RentSchedule
from .serializers import PaymentMethodSerializer, PaymentStatusSerializer, PaymentSerializer, PaymentHistorySerializer, RentScheduleSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class PaymentStatusViewSet(viewsets.ModelViewSet):
    queryset = PaymentStatus.objects.filter(is_active=True)
    serializer_class = PaymentStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['receipt_number', 'transaction_id', 'tenant__first_name', 'tenant__last_name']
    ordering_fields = ['payment_date', 'due_date', 'amount', 'created_at']
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        lease = self.request.query_params.get('lease', None)
        tenant = self.request.query_params.get('tenant', None)
        payment_method = self.request.query_params.get('payment_method', None)
        payment_status = self.request.query_params.get('payment_status', None)
        
        if lease:
            queryset = queryset.filter(lease_id=lease)
        if tenant:
            queryset = queryset.filter(tenant_id=tenant)
        if payment_method:
            queryset = queryset.filter(payment_method_id=payment_method)
        if payment_status:
            queryset = queryset.filter(payment_status_id=payment_status)
        
        return queryset

class PaymentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['changed_at']
    
    def get_queryset(self):
        queryset = PaymentHistory.objects.all()
        payment = self.request.query_params.get('payment', None)
        
        if payment:
            queryset = queryset.filter(payment_id=payment)
        
        return queryset

class RentScheduleViewSet(viewsets.ModelViewSet):
    queryset = RentSchedule.objects.all()
    serializer_class = RentScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date', 'created_at']
    
    def get_queryset(self):
        queryset = RentSchedule.objects.all()
        lease = self.request.query_params.get('lease', None)
        status = self.request.query_params.get('status', None)
        
        if lease:
            queryset = queryset.filter(lease_id=lease)
        if status:
            queryset = queryset.filter(status_id=status)
        
        return queryset

