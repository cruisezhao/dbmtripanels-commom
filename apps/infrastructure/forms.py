from django import forms
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections,DEVICE_TYPE,DataCenters)
from datetimewidget.widgets import DateTimeWidget, DateWidget


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
        fields = ['name','manufacturer','model',
                  'sn','rack','u_height','tag','seller','purchase_date',
                  'price', 'order_no','warranty_date','status',
                  'data_center','total_electric_current',
                  'used_electric_current','ec_check_date','power_stripe_amount',
                  'total_band_width','used_band_width', 'bw_check_date',
                  'up_router_ip','comments','location']


class DataCentersForm(forms.ModelForm):
    class Meta:
        model =DataCenters
        fields = ['name','tag','address','city','state',
                  'country','zip','website','phone','support_email',
                  'support_portal','username','password','notes']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = ['name', 'type', 'description','website','status']


class DevicePowerForm(DeviceDateForm):
    class Meta:
        model = DevicePowers
        fields = ['data_center','name','type','model','manufacturer','sn',
                  'rack','u_height','tag','seller', 'purchase_date', 'price',
                  'order_no', 'warranty_date', 'status', 'comments',
                  'outlet_amount', 'voltage', 'mgmt_ip']


class DeviceDriveForm(DeviceDateForm):
    class Meta:
        model = DeviceDrives
        fields = ['data_center','name','type','model','manufacturer','sn',
                  'rack','u_height','tag','seller', 'purchase_date', 'price',
                  'order_no', 'warranty_date', 'status', 'comments',
                  'disk_size','file_system']


class DeviceKVMForm(DeviceDateForm):
    class Meta:
        model = DeviceKVMs
        fields = ['data_center','name','type','model','manufacturer','sn',
                  'rack','u_height','tag','seller', 'purchase_date', 'price',
                  'order_no', 'warranty_date', 'status', 'comments',
                  'account', 'password', 'mgmt_ip', 'port_amount']


class DeviceRouterForm(DeviceDateForm):
    class Meta:
        model = DeviceRouters
        fields = ['data_center','name','type','model','manufacturer','sn',
              'rack','u_height','tag','seller', 'purchase_date', 'price',
              'order_no', 'warranty_date', 'status', 'comments',
              'account', 'password', 'mgmt_ip','os_version', 'port_amount']


class DeviceSwitcheForm(DeviceDateForm):
     class Meta:
        model = DeviceSwitches
        fields = ['data_center','name','type','model','manufacturer','sn',
              'rack','u_height','tag','seller', 'purchase_date', 'price',
              'order_no', 'warranty_date', 'status', 'comments',
              'account', 'password', 'mgmt_ip','os_version', 'port_amount']


class DeviceFirewallForm(DeviceDateForm):
    class Meta:
        model = DeviceFirewalls
        fields = ['data_center','name','type','model','manufacturer','sn',
              'rack','u_height','tag','seller', 'purchase_date', 'price',
              'order_no', 'warranty_date', 'status', 'comments',
              'account', 'password', 'mgmt_ip','os_version', 'port_amount',
                'license_amount','safe_area','unsafe_area']


class DeviceBareForm(DeviceDateForm):

    class Meta:
        model = DeviceBares
        fields = ['data_center',]



#     'name','type','model','manufacturer','sn',
# 'rack','u_height','tag','seller', 'purchase_date', 'price',
# 'order_no', 'warranty_date', 'status', 'comments',
# 'account', 'password', 'mgmt_ip', 'port_amount',
# 'processor_model','no_of_processors','memory_chips','memory_size','motherboard_model',
#   'chassis_model', 'power_supply_model', 'disk_size',
#     'disk_description'
#   ]
