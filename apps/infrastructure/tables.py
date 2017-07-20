import django_tables2 as tables
from django_tables2.utils import A
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)
from common.utilities.tables import ToggleColumn

class RackTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:rack", args=[A('uuid')])
    class Meta:
        model = DeviceRacks
        fields = ['pk','name','manufacturer','data_center', 'location','power_stripe_amount']


class DataCenterTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:data_center", args=[A('uuid')])
    class Meta:
        model = DataCenters
        fields = ['pk', 'name', 'address','website','phone','support_email','username']


class VerdorTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:vendor", args=[A('uuid')])

    class Meta:
        model = Vendors
        fields = ['pk', 'name', 'type', 'description', 'website', 'status']


class DevicePowerTable(tables.Table):
    pk = ToggleColumn()
    name= tables.LinkColumn('infras:power', args=[A("uuid")])

    class Meta:
        model = DevicePowers
        fields = ['pk','name','outlet_amount','voltage','mgmt_ip']


class DeviceDriveTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn('infras:driver', args=[A("uuid")])

    class Meta:
        model = DeviceDrives
        fields = ['pk','name','disk_size','file_system']