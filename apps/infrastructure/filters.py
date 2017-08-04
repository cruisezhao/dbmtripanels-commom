import django_filters
from .models.network import (Devices, DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)
from .models.ip import VLANs, IPPrefixes, IPAddresses, IPInterfaces

class RackFilter(django_filters.FilterSet):
    """rack filter"""
    data_center_id = django_filters.ModelMultipleChoiceFilter(
        name='data_center__pk',
        to_field_name='pk',
        queryset=DataCenters.objects.all(),
        label='Data_Center (ID)',
    )
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


class DeviceFirewallFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceFirewalls
        fields = ['name']


class DeviceBareFilter(django_filters.FilterSet):
    class Meta:
        model = DeviceBares
        fields = ['name']


class DeviceMaintenanceFilter(django_filters.FilterSet):

    class Meta:
        model = DeviceMaintenances
        fields = ['user']


class InterfaceRackFilter(django_filters.FilterSet):

    class Meta:
        model = InterfaceRacks
        fields = ['name', 'device']


class InterfaceNetworkFilter(django_filters.FilterSet):
    class Meta:
        model = InterfaceNetworks
        fields = ['name', 'device']


class ConnectionFilter(django_filters.FilterSet):
    class Meta:
        model = Connections
        fields = ['type', 'status']


class VlanFilter(django_filters.FilterSet):
    """vlan filter
    """
    device_id = django_filters.ModelMultipleChoiceFilter(
        name='device__pk',
        to_field_name='pk',
        queryset=Devices.objects.all(),
        label='Device (ID)',
    )
    class Meta:
        model =VLANs
        fields = ['name']


class IPPrefixFilter(django_filters.FilterSet):
    class Meta:
        model =IPPrefixes
        fields = ['type']


class IPAddressFilter(django_filters.FilterSet):
    class Meta:
        model =IPAddresses
        fields = ['status']