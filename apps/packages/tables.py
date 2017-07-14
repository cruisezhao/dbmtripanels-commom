'''
Created on Jul 5, 2017

@author: ben
'''

import django_tables2 as tables
from common.apps.packages.models import Packages
from django_tables2 import A
from common.utilities.tables import ToggleColumn

DEPLOY_ACTIONS = """
{% if record.status == 'Pending' %}
    <a href="{% url 'deployments:deploy' record.uuid %}" class="btn btn-xs btn-warning">deploy</a>
{% endif %}
"""

class PackageTable(tables.Table):
    """Package table"""
    pk = ToggleColumn()
    id = tables.LinkColumn('packages:detail', args=[A('uuid')])
    package_name = tables.Column()
    created = tables.Column()
    client = tables.Column(accessor='client.email')
    status = tables.Column()
    deploy = tables.TemplateColumn(
        template_code=DEPLOY_ACTIONS,
        attrs={'td': {'class': 'text-right'}},
        verbose_name=''
    )    

    class Meta:
        model = Packages
        fields = ('pk','id','package_name','created','client', 'status',)
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }