# inventory/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    class LocationType(models.TextChoices):
        HEADQUARTERS = 'HQ', 'Headquarters'
        BRANCH = 'BR', 'Branch'

    city            = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')
    location_type   = models.CharField(max_length=2, choices=LocationType.choices)
    street          = models.CharField(max_length=255)
    building_number = models.CharField(max_length=20)
    name            = models.CharField(max_length=100, help_text='e.g. "Branch #1" or "Main HQ"')

    class Meta:
        ordering = ['city', 'name']

    def __str__(self):
        return f'{self.name} — {self.city}, {self.street} {self.building_number}'


class NetworkEquipment(models.Model):
    class EquipmentType(models.TextChoices):
        ROUTER = 'router', 'Router'
        SWITCH = 'switch', 'Switch'
        AP     = 'ap',     'Access Point'
        OTHER  = 'other',  'Other'

    location         = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='equipment')
    equipment_type   = models.CharField(max_length=10, choices=EquipmentType.choices)
    brand            = models.CharField(max_length=100)
    model_name       = models.CharField(max_length=100)
    ip_address       = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    mac_address      = models.CharField(max_length=17, unique=True,
                                        help_text='Format: AA:BB:CC:DD:EE:FF')
    serial_number    = models.CharField(max_length=100, unique=True)
    inventory_number = models.CharField(max_length=100, unique=True)
    notes            = models.TextField(blank=True)
    created_by       = models.ForeignKey(User, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='equipment')

    class Meta:
        verbose_name_plural = 'Network Equipment'
        ordering = ['location', 'equipment_type', 'brand']

    def __str__(self):
        return (f'[{self.get_equipment_type_display()}] '
                f'{self.brand} {self.model_name} — {self.ip_address}')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)