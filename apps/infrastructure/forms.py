from django import forms
from .models.network import (Devices,DeviceRacks,DataCenters,Vendors,InterfaceRacks,Interfaces,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections,DataCenters)
from datetimewidget.widgets import DateTimeWidget, DateWidget
from .utilities.forms import \
    (DeviceComponentForm, ExpandableNameField,
    ChainedModelChoiceField, APISelect, ChainedFieldsMixin)
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


class DevicePowerForm(forms.ModelForm):
    class Meta:
        model = DevicePowers
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'total_outlets', 'max_amps', 'used_amps','check_date',
                  'voltage','color']


class DeviceDriveForm(forms.ModelForm):
    class Meta:
        model = DeviceDrives
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'disk_type','disk_size','file_system','need_power']


class DeviceKVMForm(forms.ModelForm):
    class Meta:
        model = DeviceKVMs
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'total_ports', 'port_type']


class DeviceRouterForm(forms.ModelForm):
    class Meta:
        model = DeviceRouters
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version', 'total_ports', 'speed']


class DeviceSwitcheForm(forms.ModelForm):
     class Meta:
        model = DeviceSwitches
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version','total_ports','speed']


class DeviceFirewallForm(forms.ModelForm):
    class Meta:
        model = DeviceFirewalls
        fields = ['data_center','manufacturer','seller','name','tag',
                  'description', 'type','u_height','size','model_no',
                  'serial_no','online_date','offline_date','order_date',
                  'price','order_no','warranty_date','access_method',
                  'access_port','username','password','status','notes',
                  'firmware_version', 'total_ports', 'total_licenses','speed',]


class DeviceBareForm(forms.ModelForm):

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


class DeviceMaintenanceForm(forms.ModelForm):

    class Meta:
        model = DeviceMaintenances
        fields = ['device', 'user', 'start_time','end_time','subject',
                  'description','status','notes']


class InterfaceCreateForm(DeviceComponentForm):
    name_pattern = ExpandableNameField(label='Name')
    tag_pattern = ExpandableNameField(label='Tag', required=False)
    type = forms.ChoiceField(choices=Interfaces.INTERFACE_TYPE)
    index_pattern = ExpandableNameField(label='Index', required=False,help_text = 'Numeric ranges are supported for bulk creation.<br />'\
                             'Example: <code>[0-23,25,30]</code><br />'\
                             'Only support integer elements here.')
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

    def clean(self):
        cleaned_data = super().clean()
        name_pattern = cleaned_data.get("name_pattern")
        tag_pattern = cleaned_data.get("tag_pattern")
        index_pattern = cleaned_data.get("index_pattern")
        if not len(tag_pattern)==len(name_pattern)==len(index_pattern):
            raise forms.ValidationError("Name,Tag and Index should have the same amount.")


    class Groups:
        from collections import OrderedDict
        groups = OrderedDict([('Rack', ('has_rail', 'rail_model')), ('Network', ('port_model', 'port_fast', 'speed', 'mac'))])

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


class VlanForm(ChainedFieldsMixin, forms.ModelForm):

    data_center = forms.ModelChoiceField(
        queryset=DataCenters.objects.all(),
        widget=forms.Select(
            attrs={'filter-for': 'device'}
        )
    )
    device = ChainedModelChoiceField(
        queryset=Devices.objects.all(),
        chains=(
            ('data_center', 'data_center'),
        ),
        required=False,
        widget=APISelect(
            api_url='/api/device/devices/?data_center_id={{data_center}}',
        )
    )
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