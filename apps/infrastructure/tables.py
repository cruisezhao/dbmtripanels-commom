import django_tables2 as tables
from django_tables2.utils import A
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)
from common.utilities.tables import ToggleColumn
from .models.ip import VLANs, IPPrefixes, IPAddresses, IPInterfaces

class RackTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:rack", args=[A('uuid')])
    class Meta:
        model = DeviceRacks
        fields = ['pk','name','data_center','manufacturer', 'location','network_tag']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DataCenterTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:data_center", args=[A('id')])
    class Meta:
        model = DataCenters
        fields = ['pk', 'name', 'address','website','phone','support_email','username']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class VerdorTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:vendor", args=[A('id')])

    class Meta:
        model = Vendors
        fields = ['pk', 'name', 'type', 'description', 'website', 'status']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DevicePowerTable(tables.Table):
    pk = ToggleColumn()
    name= tables.LinkColumn('infras:power', args=[A("uuid")])

    class Meta:
        model = DevicePowers
        fields = ['pk','name','outlet_amount','voltage','mgmt_ip']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DeviceDriveTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn('infras:driver', args=[A("uuid")])

    class Meta:
        model = DeviceDrives
        fields = ['pk','name','disk_size','file_system']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DeviceKVMTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:kvm", args=[A("uuid")])
    class Meta:
        model = DeviceKVMs
        fields = ['pk','name','account', 'password', 'mgmt_ip', 'port_amount']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DeviceRouterTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:router", args=[A("uuid")])

    class Meta:
        model = DeviceRouters
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }

class DeviceSwitcheTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:switch", args=[A("uuid")])
    class Meta:
        model = DeviceRouters
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DeviceFirewallTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:firewall", args=[A("uuid")])
    class Meta:
        model = DeviceFirewalls
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount',
                  'license_amount','safe_area','unsafe_area']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }

class DeviceBareTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:bare", args=[A("uuid")])
    class Meta:
        model = DeviceFirewalls
        fields = ['pk','name','account', 'password', 'mgmt_ip','os_version', 'port_amount',
                  'processor_model','no_of_processors','memory_chips','memory_size','motherboard_model',]
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class DeviceMaintenanceTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn("infras:device_maintenance", args=[A("uuid")])

    class Meta:
        model = DeviceMaintenances
        fields = ['pk','id','device', 'user', 'start_time','end_time',
                  'task_subject','task_detail','total_minutes','status','notes']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class InterfaceRackTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:interface_rack", args=[A("uuid")])


    class Meta:
        model = InterfaceRacks
        fields = ['pk','name', 'device', 'tag', 'type', 'status', 'description',
                  'has_rail', 'rail_model', 'unit_no']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class InterfaceNetworkTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:interface_network", args=[A("uuid")])

    class Meta:
        model = InterfaceNetworks
        fields = ['pk','name', 'device', 'tag', 'type', 'status', 'description',
                  'speed', 'mac', 'port_model']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class ConnectionTable(tables.Table):
    pk = ToggleColumn()
    type = tables.LinkColumn("infras:connection", args=[A("uuid")])

    class Meta:
        model = Connections
        fields = ['pk','interface_a', 'interface_b', 'type', 'status', 'description']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }

STATUS_LABEL = """
    <span class="label label-{{record.get_status_class}}">{{ record.status }}</span>
"""
class VlanTable(tables.Table):
    pk = ToggleColumn()
    name = tables.LinkColumn("infras:vlan", args=[A("id")])
    data_center = tables.LinkColumn("infras:data_center", args=[A('data_center.id')])
    device = tables.LinkColumn(A('get_device_url'), args=[A('device.uuid')])
    status = tables.TemplateColumn(STATUS_LABEL)
    class Meta:
        model = VLANs
        fields = ['pk', 'name','data_center','device','vid','status']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class IPPrefixTable(tables.Table):
    pk = ToggleColumn()
    prefix = tables.LinkColumn("infras:prefix", args=[A("id")])
    data_center = tables.LinkColumn("infras:data_center", args=[A('data_center.id')])
    device = tables.LinkColumn(A('get_device_url'), args=[A('device.uuid')])
    vlan = tables.LinkColumn("infras:vlan", args=[A("vlan.id")])
    online_date = tables.DateColumn(format="Y-m-d")
    status = tables.TemplateColumn(STATUS_LABEL)

    class Meta:
        model = IPPrefixes
        fields = ['pk', 'prefix', 'type','status','data_center','device','vlan','online_date']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }


class IPAddressTable(tables.Table):
    pk = ToggleColumn()
    address = tables.LinkColumn("infras:ip_address", args=[A("id")])
    prefix = tables.LinkColumn("infras:prefix", args=[A("prefix.id")])
    status = tables.TemplateColumn(STATUS_LABEL)

    class Meta:
        model = IPAddresses
        fields = ['pk', 'address','status','prefix','nat_address']
        attrs = {
            'class':'table table-hover table-striped dataTable',
        }
