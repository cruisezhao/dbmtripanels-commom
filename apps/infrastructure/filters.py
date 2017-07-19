import django_filters
from .models.network import DeviceRacks

class RackFilter(django_filters.FilterSet):
    """rack filter"""
    class Meta:
        model = DeviceRacks
        fields = ['name']