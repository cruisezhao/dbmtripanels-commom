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
    name = tables.LinkColumn("infras:data_center", args=[A('id')])
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


class DeviceKVMTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:kvm", args=[A("uuid")])
    class Meta:
        model = DeviceKVMs
        fields = ['pk','name','account', 'password', 'mgmt_ip', 'port_amount']


class DeviceRouterTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:router", args=[A("uuid")])

    class Meta:
        model = DeviceRouters
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount']

class DeviceSwitcheTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:switche", args=[A("uuid")])
    class Meta:
        model = DeviceRouters
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount']


class DeviceFirewallTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:firewall", args=[A("uuid")])
    class Meta:
        model = DeviceFirewalls
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount',
                  'license_amount','safe_area','unsafe_area']

class DeviceBareTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:bare", args=[A("uuid")])
    class Meta:
        model = DeviceFirewalls
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount',
                  'processor_model','no_of_processors','memory_chips','memory_size','motherboard_model',]


class DeviceMaintenanceTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn("infras:device_maintenance", args=[A("uuid")])

    class Meta:
        model = DeviceMaintenances
        fields = ['pk','id','device', 'user', 'start_time','end_time',
                  'task_subject','task_detail','total_minutes','status','notes']


class InterfaceRackTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:interface_rack", args=[A("uuid")])

    class Meta:
        model = InterfaceRacks
        fields = ['pk','name', 'device', 'tag', 'type', 'status', 'description',
                  'has_rail', 'rail_model', 'unit_no']


class InterfaceNetworkTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:interface_network", args=[A("uuid")])

    class Meta:
        model = InterfaceNetworks
        fields = ['pk','name', 'device', 'tag', 'type', 'status', 'description',
                  'speed', 'mac', 'port_model']


class ConnectionTable(tables.Table):
    pk = ToggleColumn()
    type = tables.LinkColumn("infras:connection", args=[A("uuid")])

    class Meta:
        model = Connections
        fields = ['pk','interface_a', 'interface_b', 'type', 'status', 'description']