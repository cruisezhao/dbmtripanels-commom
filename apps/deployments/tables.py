import django_tables2 as tables
from django_tables2.utils import A
from .models import SystemOptions

class SysOptionTable(tables.Table):
    id = tables.LinkColumn('sys_option', args=[A('uuid')])

    class Meta:
        model = SystemOptions
        fields = ['id', 'name', 'value']