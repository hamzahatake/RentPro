from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingTypeViewSet, BuildingViewSet, UnitTypeViewSet, UnitStatusViewSet, AmenityViewSet, UnitViewSet, UnitImageViewSet

router = DefaultRouter()
router.register(r'building-types', BuildingTypeViewSet, basename='building-type')
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'unit-types', UnitTypeViewSet, basename='unit-type')
router.register(r'unit-statuses', UnitStatusViewSet, basename='unit-status')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'unit-images', UnitImageViewSet, basename='unit-image')

urlpatterns = [
    path('', include(router.urls)),
]

