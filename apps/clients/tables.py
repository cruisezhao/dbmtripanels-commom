import django_tables2 as tables
from django_tables2.utils import A
from .models import Clients

class ClientTable(tables.Table):
    """product table"""
    # DETAIL_URL_NAME = 'clients'
    # id = tables.LinkColumn(DETAIL_URL_NAME, args=[A('uuid')])
    email = tables.EmailColumn()

    class Meta:
        model = Clients
        fields = ('pk','first_name','last_name','email','status',
                  'phone_number','user_type')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }