# inventory/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CityViewSet, LocationViewSet, NetworkEquipmentViewSet, UserViewSet, login_view

router = DefaultRouter()
router.register(r'cities',    CityViewSet,             basename='city')
router.register(r'locations', LocationViewSet,         basename='location')
router.register(r'equipment', NetworkEquipmentViewSet, basename='equipment')
router.register(r'users',     UserViewSet,             basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
]