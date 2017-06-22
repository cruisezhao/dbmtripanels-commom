"""crud for soft ware and product"""

from .models import Products, Video, Screenshot, Plans
from crudbuilder.abstract import BaseCrudBuilder
from crudbuilder.formset import BaseInlineFormset
from django.db.models import Q
from functools import reduce
import operator
from common.utilities.crud_mixin import CrudContextMixin,CrudQuerySetMixin
# from .tables import SoftwareTable

class VideoInlineFormset(BaseInlineFormset):
    """video information display in software table"""
    inline_model = Video
    # parent_model = Software


class ScreenshotInlineFormset(BaseInlineFormset):
    """screenshot information display in software table"""
    inline_model = Screenshot
    # parent_model = Software


class ProductCRUD(BaseCrudBuilder,CrudContextMixin, CrudQuerySetMixin):
    """product crud"""
    model = Products
    search_fields = ['version', 'title','system','database','created_date','updated_date']
    tables2_fields = ('product_type','product_name', 'created','last_updated')
    tables2_css_class = "table table-bordered table-condensed"
    modelform_excludes = ('created_by','updated_by')
    custom_table2 = None
    tables2_pagination = 5
    login_required=False
    permission_required=False

    custom_templates = {
        'detail': 'applications/product_detail.html',
        'list': 'applications/product_list.html',
        'update': 'applications/product_update.html',
    }

    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """add context of search"""
        context['search_fields'] = ['version','title','system','created_date',]
        context['extra_button'] = True
        return context


class PlansCrud(BaseCrudBuilder, CrudContextMixin, CrudQuerySetMixin):
    """plans crud"""
    model = Plans
    search_fields = ['name', 'created','last_updated']
    tables2_fields = ('name', 'cpu','memory','disk', 'instance', 'created','last_updated','price')
    tables2_css_class = "table table-bordered table-condensed"
    modelform_excludes = ('created_by','updated_by')
    tables2_pagination = 5
    login_required=False
    permission_required=False

    custom_templates = {
        'detail': 'products/plan_detail.html',
        'list': 'products/plan_list.html',
        'update': 'products/plan_update.html',
        'create': 'products/plan_create.html',
        'delete': 'products/plan_delete.html',
    }

    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """overide context"""
        context.update({'extra_button':True})
        context['search_fields'] = cls.search_fields
        return context
