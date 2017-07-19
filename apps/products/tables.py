"""custom tables for applications"""

import django_tables2 as tables
from django_tables2.utils import A
from common.apps.products.models import Products, Plans
from common.utilities.tables import ToggleColumn


class ProductTable(tables.Table):
    """product table"""
    DETAIL_URL_NAME = 'product'
    pk = ToggleColumn()
    product_name = tables.LinkColumn(DETAIL_URL_NAME, args=[A('uuid')])
    plans = tables.Column(accessor='all_plans', orderable=False)
    summary = tables.Column(
        accessor='get_model.summary',
        orderable=False
    )

    class Meta:
        model = Products
        fields = ('pk','product_name','plans','product_type','summary',
                  'created','last_updated')
        # sequence = ('selection', 'summary')+fields
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }


class PlanTable(tables.Table):
    """plan table"""
    """product table"""
    pk = ToggleColumn()
    id = tables.LinkColumn('plan', args=[A('uuid')])

    class Meta:
        model = Plans
        fields = ('pk','id','name','cpu','memory','disk','instance', 'price',
                  'created','last_updated')
