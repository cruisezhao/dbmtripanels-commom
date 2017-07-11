import django_tables2 as tables
from django_tables2.utils import A
from .models import Clients

class ClientTable(tables.Table):
    """product table"""
    # DETAIL_URL_NAME = 'clients'
    # id = tables.LinkColumn(DETAIL_URL_NAME, args=[A('uuid')])
    email = tables.EmailColumn()
    phone_number = tables.Column()

    class Meta:
        model = Clients
        fields = ('pk','first_name','last_name','email','phone_number','status','user_type')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }