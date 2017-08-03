from rest_framework import viewsets
from ..models.network import DeviceRacks
from .. import filters
from . import serializers

class DeviceRacksViewSet(viewsets.ModelViewSet):
    """device view set"""
    queryset  = DeviceRacks.objects.all()
    serializer_class = serializers.DeviceSerializer
    filter_class = filters.RackFilter
    # filter_fields = ('id',)