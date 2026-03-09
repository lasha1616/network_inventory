# inventory/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import City, Location, NetworkEquipment


# ── User ──────────────────────────────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active',
                  'date_joined', 'password']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ── NetworkEquipment ──────────────────────────────────────────────────────────

class NetworkEquipmentSerializer(serializers.ModelSerializer):
    equipment_type_display = serializers.CharField(
        source='get_equipment_type_display', read_only=True
    )
    created_by_username = serializers.CharField(
        source='created_by.username', read_only=True
    )

    class Meta:
        model  = NetworkEquipment
        fields = [
            'id', 'location', 'equipment_type', 'equipment_type_display',
            'brand', 'model_name', 'ip_address', 'mac_address',
            'serial_number', 'inventory_number', 'notes',
            'created_by', 'created_by_username',
        ]
        read_only_fields = ['created_by']

# ── Location ──────────────────────────────────────────────────────────────────

class LocationSerializer(serializers.ModelSerializer):
    equipment            = NetworkEquipmentSerializer(many=True, read_only=True)
    location_type_display = serializers.CharField(
        source='get_location_type_display', read_only=True
    )
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model  = Location
        fields = [
            'id', 'city', 'city_name', 'location_type', 'location_type_display',
            'street', 'building_number', 'name', 'equipment',
        ]


# ── City ──────────────────────────────────────────────────────────────────────

class CitySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model  = City
        fields = ['id', 'name', 'locations']
