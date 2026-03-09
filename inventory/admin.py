# inventory/admin.py
from django.contrib import admin
from .models import City, Location, NetworkEquipment


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'city', 'location_type', 'street', 'building_number']
    list_filter   = ['location_type', 'city']
    search_fields = ['name', 'street', 'city__name']


@admin.register(NetworkEquipment)
class NetworkEquipmentAdmin(admin.ModelAdmin):
    list_display    = ['equipment_type', 'brand', 'model_name', 'ip_address',
                       'mac_address', 'inventory_number', 'location', 'created_by']
    list_filter     = ['equipment_type', 'brand', 'location__city']
    search_fields   = ['brand', 'model_name', 'ip_address',
                       'mac_address', 'serial_number', 'inventory_number']
    readonly_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)