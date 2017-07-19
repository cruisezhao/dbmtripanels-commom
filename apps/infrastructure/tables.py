import django_tables2 as tables
from django_tables2.utils import A
from .models.network import DeviceRacks

class RackTable(tables.Table):
    name = tables.LinkColumn("infras:rack", args=[A('uuid')])
    class Meta:
        model = DeviceRacks
        fields = ['name','manufacturer','data_center', 'location','power_stripe_amount']