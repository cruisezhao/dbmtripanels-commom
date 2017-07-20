from django import forms
from .models.network import DeviceRacks,Vendors,DEVICE_TYPE
from datetimewidget.widgets import DateTimeWidget, DateWidget

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