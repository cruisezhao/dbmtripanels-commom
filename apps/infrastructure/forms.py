from django import forms
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,Interfaces,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections,DataCenters)
from datetimewidget.widgets import DateTimeWidget, DateWidget
from .utilities.forms import DeviceComponentForm
from .models.ip import VLANs, IPPrefixes, IPAddresses, IPInterfaces


class DeviceDateForm(forms.ModelForm):
    purchase_date = forms.DateField(
        required=False,
        label='Purchase Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )

    warranty_date = forms.DateField(
        required=False,
        label='Warranty Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )


class DeviceRacksForm(forms.ModelForm):
    """"""
    # seller = forms.ModelChoiceField(queryset = Vendors.objects.all(), required=False)
    # status = forms.ChoiceField(choices = DEVICE_TYPE)
    purchase_date = forms.DateField(
        required=False,
        label='Purchase Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    ec_check_date = forms.DateField(
        required=False,
        label='EC Check Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    warranty_date = forms.DateField(
        required=False,
        label='Warranty Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    bw_check_date = forms.DateField(
        required=False,
        label='BW Check Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    class Meta:
        model = DeviceRacks
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'location','network_tag','network_speed','max_bandwidth',
                  'used_bandwidth','bw_check_date','routing_ip','routing_gateway',
                  'routing_mask']


class DataCentersForm(forms.ModelForm):
    class Meta:
        model =DataCenters
        fields = ['name','description','address','region','city',
                  'state','country','zip','website','phone','support_email',
                  'support_portal','username','password','status','notes']




class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = ['name', 'type', 'description','website','status']


class DevicePowerForm(DeviceDateForm):
    class Meta:
        model = DevicePowers
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'total_outlets', 'max_amps', 'used_amps','check_date',
                  'voltage','color']


class DeviceDriveForm(DeviceDateForm):
    class Meta:
        model = DeviceDrives
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'disk_type','disk_size','file_system','need_power']


class DeviceKVMForm(DeviceDateForm):
    class Meta:
        model = DeviceKVMs
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'total_ports', 'port_type']


class DeviceRouterForm(DeviceDateForm):
    class Meta:
        model = DeviceRouters
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version', 'total_ports', 'speed']


class DeviceSwitcheForm(DeviceDateForm):
     class Meta:
        model = DeviceSwitches
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version','total_ports','speed']


class DeviceFirewallForm(DeviceDateForm):
    class Meta:
        model = DeviceFirewalls
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version', 'total_ports', 'total_licenses','speed',]


class DeviceBareForm(DeviceDateForm):

    class Meta:
        model = DeviceBares
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'memory_model', 'memory_size', 'motherboard_model',
                  'chassis_model','power_supply_model','disk_size',
                  'disk_description','has_raid','raid_type','has_ipmi',
                  'ipmi_username', 'ipmi_password','ipmi_version','total_ports',
                  'firmware_type','firmware_version','usage']


class DeviceMaintenanceForm(DeviceDateForm):
    start_time = forms.DateTimeField(
        required=False,
        label='Start Date',
        widget=DateTimeWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_time = forms.DateTimeField(
        required=False,
        label='End Date',
        widget=DateTimeWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    class Meta:
        model = DeviceMaintenances
        fields = ['device', 'user', 'start_time','end_time','subject',
                  'description','status','notes']


class InterfaceCreateForm(DeviceComponentForm):
    name = forms.CharField(max_length=100, required=False)
    tag = forms.CharField(max_length=100, required=False)
    type = forms.ChoiceField(choices=Interfaces.INTERFACE_TYPE)
    index = forms.IntegerField(required=False)
    #rack interface attr
    has_rail = forms.BooleanField(required=False, label='Has Rail')
    rail_model = forms.CharField(max_length=100, required=False)
    #network interface attr
    port_model = forms.ChoiceField(choices=InterfaceNetworks.NETWORK_PORT_MODEL)
    port_fast = forms.BooleanField(required=False, label='Port Fast')
    speed = forms.IntegerField(required=False)
    mac = forms.CharField(max_length=100, required=False)

    status = forms.ChoiceField(choices=Interfaces.INTERFACE_STATUS)
    description = forms.CharField(max_length=100, required=False)
    notes = forms.CharField(max_length=100, required=False)

    class Groups:
        from collections import OrderedDict
        groups = OrderedDict([('Group1', ('has_rail', 'rail_model')), ('Group2', ('port_model', 'port_fast', 'speed', 'mac'))])

class InterfaceRackForm(forms.ModelForm):
    class Meta:
        model = InterfaceRacks
        fields = ['device', 'tag', 'type','name','index','description','status', 'notes',
                  'has_rail','rail_model', ]

class InterfaceNetworkForm(forms.ModelForm):
     class Meta:
        model = InterfaceNetworks
        fields = ['device', 'tag', 'type','name','index','description','status', 'notes',
                  'port_model', 'port_fast', 'port_type','speed','mac']


class InterfaceForm(forms.ModelForm):
    class Meta:
        model = Interfaces
        fields = ['device', 'tag', 'type', 'name', 'index', 'description', 'status', 'notes']


class ConnectionForm(forms.ModelForm):

    class Meta:
        model = Connections
        fields = ['interface_a', 'interface_b', 'type', 'status', 'description','notes']


class VlanForm(forms.ModelForm):

    class Meta:
        model = VLANs
        fields = ['data_center', 'device', 'name', 'description', 'vid','status','notes']


class IPPrefixForm(forms.ModelForm):
    class Meta:
        model = IPPrefixes
        fields = ['data_center', 'device', 'vlan','family',
                  'type','prefix','notation','gateway_ip',
                  'net_mask','description','start_ip','end_ip','online_date',
                  'offline_date','status','notes']


class IPAddressForm(forms.ModelForm):
    class Meta:
        model = IPAddresses
        fields = ['prefix', 'address', 'nat_address',
                  'description','status','notes']