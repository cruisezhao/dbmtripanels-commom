'''
Created on Jul 5, 2017

@author: ben
'''

import django_tables2 as tables
from common.apps.packages.models import Packages
from django_tables2 import A

class PackageTable(tables.Table):
    """Package table"""
    id = tables.LinkColumn('packages:detail', args=[A('uuid')])
    package_name = tables.Column()
    created = tables.Column()
    client = tables.Column(accessor='client.email')
    status = tables.Column()
    

    class Meta:
        model = Packages
        fields = ('id','package_name','created','client', 'status')
        attrs={
                "class": "table table-bordered table-condensed table-hover",
            }