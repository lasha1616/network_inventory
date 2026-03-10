from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import City, Location, NetworkEquipment
from .serializers import (
    CitySerializer, LocationSerializer,
    NetworkEquipmentSerializer, UserSerializer,
)
from .permissions import IsAdminOrReadOnly, IsAdminOrOwner


@extend_schema_view(
    list=extend_schema(tags=['cities']),
    create=extend_schema(tags=['cities']),
    retrieve=extend_schema(tags=['cities']),
    update=extend_schema(tags=['cities']),
    partial_update=extend_schema(tags=['cities']),
    destroy=extend_schema(tags=['cities']),
)
class CityViewSet(viewsets.ModelViewSet):
    queryset           = City.objects.prefetch_related('locations__equipment').all()
    serializer_class   = CitySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name']
    ordering_fields    = ['name']


@extend_schema_view(
    list=extend_schema(tags=['locations']),
    create=extend_schema(tags=['locations']),
    retrieve=extend_schema(tags=['locations']),
    update=extend_schema(tags=['locations']),
    partial_update=extend_schema(tags=['locations']),
    destroy=extend_schema(tags=['locations']),
)
class LocationViewSet(viewsets.ModelViewSet):
    queryset           = Location.objects.select_related('city').prefetch_related('equipment').all()
    serializer_class   = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'street', 'city__name']
    ordering_fields    = ['name', 'city__name', 'location_type']

    def get_queryset(self):
        qs = super().get_queryset()
        city_id = self.request.query_params.get('city')
        if city_id:
            qs = qs.filter(city_id=city_id)
        loc_type = self.request.query_params.get('type')
        if loc_type:
            qs = qs.filter(location_type=loc_type)
        return qs


@extend_schema_view(
    list=extend_schema(tags=['equipment']),
    create=extend_schema(tags=['equipment']),
    retrieve=extend_schema(tags=['equipment']),
    update=extend_schema(tags=['equipment']),
    partial_update=extend_schema(tags=['equipment']),
    destroy=extend_schema(tags=['equipment']),
)
class NetworkEquipmentViewSet(viewsets.ModelViewSet):
    queryset           = NetworkEquipment.objects.select_related('location__city').all()
    serializer_class   = NetworkEquipmentSerializer
    permission_classes = [IsAdminOrOwner]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['brand', 'model_name', 'ip_address',
                          'mac_address', 'serial_number', 'inventory_number']
    ordering_fields    = ['equipment_type', 'brand', 'ip_address']

    def get_queryset(self):
        qs = super().get_queryset()
        location_id = self.request.query_params.get('location')
        if location_id:
            qs = qs.filter(location_id=location_id)
        eq_type = self.request.query_params.get('type')
        if eq_type:
            qs = qs.filter(equipment_type=eq_type)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=['users']),
    create=extend_schema(tags=['users']),
    retrieve=extend_schema(tags=['users']),
    update=extend_schema(tags=['users']),
    partial_update=extend_schema(tags=['users']),
    destroy=extend_schema(tags=['users']),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset           = User.objects.all().order_by('username')
    serializer_class   = UserSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(tags=['users'])
    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrReadOnly])
    def me(self, request):
        """Return the currently authenticated user's info."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ── Login ─────────────────────────────────────────────────────────────────────

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


@extend_schema(
    tags=['auth'],
    request=LoginSerializer,
    responses={200: {'type': 'object', 'properties': {'token': {'type': 'string'}}}}
)
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
    """Token login — exempt from CSRF so homepage can always log in."""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)