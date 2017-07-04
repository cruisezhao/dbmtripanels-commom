"""custom tables for applications"""

import django_tables2 as tables
from django_tables2.utils import A
from common.apps.products.models import Products
from common.utilities.tables import ToggleColumn


class ProductTable(tables.Table):
    """product table"""
    DETAIL_URL_NAME = 'products-productses-detail'
    pk = ToggleColumn()
    uuid = tables.LinkColumn(DETAIL_URL_NAME, args=[A('uuid')])
    plans = tables.Column(accessor='all_plans', orderable=False)
    summary = tables.Column(
        accessor='get_model.summary',
        orderable=False
    )

    class Meta:
        model = Products
        fields = ('pk','uuid','plans','product_type','product_name','summary',
                  'created','last_updated')
        # sequence = ('selection', 'summary')+fields
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }
