import django_filters
from .models.network import DeviceRacks,DataCenters,Vendors

class RackFilter(django_filters.FilterSet):
    """rack filter"""
    class Meta:
        model = DeviceRacks
        fields = ['name']

class DataCenterFilter(django_filters.FilterSet):

    class Meta:
        model = DataCenters
        fields = ['name']


class VendorFilter(django_filters.FilterSet):
    class Meta:
        model = Vendors
        fields = ['name']