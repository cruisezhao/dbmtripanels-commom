"""custom tables for applications"""


import django_tables2 as tables
from django_tables2.utils import A
from common.apps.products.models import Products


# class SoftwareTable(tables.Table):
#     """software table"""
#     DETAIL_URL_NAME = 'software_detail'
#     name=tables.LinkColumn(DETAIL_URL_NAME, args=[A('pk')])
# 
#     class Meta:
#         model=Software
#         fields=('name','type','software_url','latest_version','in_homepage','status',)
#         attrs={
#                 "class": "table table-bordered table-condensed",
#             }


class ProductTable(tables.Table):
    """product table"""
    DETAIL_URL_NAME = 'products-productses-detail'
    uuid = tables.LinkColumn(DETAIL_URL_NAME, args=[A('uuid')])
    plans = tables.Column(accessor='plans')

    class Meta:
        model = Products
        fields = ('uuid','plans','product_type','product_name', 'created','last_updated')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }