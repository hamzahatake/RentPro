from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import BuildingType, Building, UnitType, UnitStatus, Amenity, Unit, UnitImage
from .serializers import BuildingTypeSerializer, BuildingSerializer, UnitTypeSerializer, UnitStatusSerializer, AmenitySerializer, UnitSerializer, UnitImageSerializer

class BuildingTypeViewSet(viewsets.ModelViewSet):
    queryset = BuildingType.objects.filter(is_active=True)
    serializer_class = BuildingTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address__city', 'address__state']
    ordering_fields = ['name', 'created_at', 'year_built']
    
    def get_queryset(self):
        queryset = Building.objects.all()
        building_type = self.request.query_params.get('building_type', None)
        owner = self.request.query_params.get('owner', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if building_type:
            queryset = queryset.filter(building_type_id=building_type)
        if owner:
            queryset = queryset.filter(owner_id=owner)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.filter(is_active=True)
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['bedrooms', 'bathrooms', 'name']

class UnitStatusViewSet(viewsets.ModelViewSet):
    queryset = UnitStatus.objects.filter(is_active=True)
    serializer_class = UnitStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['unit_number', 'building__name']
    ordering_fields = ['unit_number', 'monthly_rent', 'created_at']
    
    def get_queryset(self):
        queryset = Unit.objects.all()
        building = self.request.query_params.get('building', None)
        unit_type = self.request.query_params.get('unit_type', None)
        status = self.request.query_params.get('status', None)
        bedrooms = self.request.query_params.get('bedrooms', None)
        bathrooms = self.request.query_params.get('bathrooms', None)
        
        if building:
            queryset = queryset.filter(building_id=building)
        if unit_type:
            queryset = queryset.filter(unit_type_id=unit_type)
        if status:
            queryset = queryset.filter(status_id=status)
        if bedrooms:
            queryset = queryset.filter(bedrooms=bedrooms)
        if bathrooms:
            queryset = queryset.filter(bathrooms=bathrooms)
        
        return queryset

class UnitImageViewSet(viewsets.ModelViewSet):
    queryset = UnitImage.objects.all()
    serializer_class = UnitImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['is_primary', 'uploaded_at']
    
    def get_queryset(self):
        queryset = UnitImage.objects.all()
        unit = self.request.query_params.get('unit', None)
        is_primary = self.request.query_params.get('is_primary', None)
        
        if unit:
            queryset = queryset.filter(unit_id=unit)
        if is_primary is not None:
            queryset = queryset.filter(is_primary=is_primary.lower() == 'true')
        
        return queryset

