import django_tables2 as tables
from django_tables2.utils import A
from .models.network import DeviceRacks, DataCenters
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