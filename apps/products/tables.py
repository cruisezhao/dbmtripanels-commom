"""custom tables for applications"""


import django_tables2 as tables
from django_tables2.utils import A
from common.apps.applications.models import Software, Product


class SoftwareTable(tables.Table):
    """software table"""
    DETAIL_URL_NAME = 'software_detail'
    name=tables.LinkColumn(DETAIL_URL_NAME, args=[A('pk')])

    class Meta:
        model=Software
        fields=('name','type','software_url','latest_version','in_homepage','status',)
        attrs={
                "class": "table table-bordered table-condensed",
            }


class ProductTable(tables.Table):
    """product table"""
    DETAIL_URL_NAME = 'applications-products-detail'
    software = tables.LinkColumn(DETAIL_URL_NAME, args=[A('pk')])
    # plans = tables.Column(accessor='plan')
    class Meta:
        model = Product
        fields = ('software','plan','version','system','database','created_date')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }