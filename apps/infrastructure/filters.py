import django_filters
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)

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


class DevicePowerFilter(django_filters.FilterSet):
    class Meta:
        model = DevicePowers
        fields = ['name']


class DeviceDriveFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceDrives
        fields = ['name']


class DeviceKVMFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceKVMs
        fields = ['name']


class DeviceRouterFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceRouters
        fields = ['name']


class DeviceSwitcheFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceSwitches
        fields = ['name']