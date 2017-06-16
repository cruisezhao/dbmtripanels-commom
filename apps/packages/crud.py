'''
Created on Apr 26, 2017

@author: Admin
'''
from crudbuilder.abstract import BaseCrudBuilder
from common.apps.packages.models import Packages
from common.apps.packages.forms import PackageForm
from common.utilities.crud_mixin import CrudContextMixin, CrudQuerySetMixin


class PackageCrud(BaseCrudBuilder,CrudContextMixin, CrudQuerySetMixin):
    model = Packages
    search_fields = ['package_name', 'status']
    tables2_fields = ('package_name','created','client','status',)
    login_required=True
    permission_required=False
    ordering = '-created'
    #modelform_excludes = ('created_by','updated_by')
    custom_modelform = PackageForm
    
    
    
    