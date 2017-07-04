'''
Created on Jul 3, 2017

@author: ben
'''
import django_tables2 as tables
from common.apps.orders.models import Orders
from django_tables2 import A

class OrderTable(tables.Table):
    """product table"""
    uuid = tables.LinkColumn('orders:detail', args=[A('uuid')])
    email = tables.Column(accessor='client.email')
    created_date = tables.Column()
    product_name = tables.Column(accessor='product.product_name')
    version = tables.Column(accessor='product.productapps.latest_version')
    cpu_cores = tables.Column(accessor='plan.cpu')
    memory = tables.Column(accessor='plan.memory')
    disk = tables.Column(accessor='plan.disk')
    remarks = tables.Column(accessor='notes')
    status = tables.Column()
    price = tables.Column(accessor='amount')

    class Meta:
        model = Orders
        fields = ('uuid','email','created_date','product_name', 'version','cpu_cores','memory','disk','remarks','status','price')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }