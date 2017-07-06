"""custom tables for applications"""

import django_tables2 as tables
from django_tables2.utils import A
from common.apps.products.models import Products
from common.utilities.tables import ToggleColumn


class ProductTable(tables.Table):
    """product table"""
    DETAIL_URL_NAME = 'home'
    # pk = ToggleColumn()
    product_name = tables.Column()
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
