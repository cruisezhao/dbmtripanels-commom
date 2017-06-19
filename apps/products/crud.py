"""crud for soft ware and product"""

from .models import Products, Video, Screenshot
from crudbuilder.abstract import BaseCrudBuilder
from crudbuilder.formset import BaseInlineFormset
from django.db.models import Q
from functools import reduce
import operator
# from .tables import SoftwareTable

class VideoInlineFormset(BaseInlineFormset):
    """video information display in software table"""
    inline_model = Video
    # parent_model = Software


class ScreenshotInlineFormset(BaseInlineFormset):
    """screenshot information display in software table"""
    inline_model = Screenshot
    # parent_model = Software


# class SoftwareCRUD(BaseCrudBuilder):
#     """software crud"""
#     model = Software
#     search_fields = ['type','name', 'status','features','environments']
#     custom_table2 = SoftwareTable
#     tables2_fields = ('type','name','software_url','latest_version','in_homepage',
#                      'status',)
#     modelform_excludes = ('status', 'in_homepage','created_by','updated_by')
#     tables2_css_class = "table table-bordered table-condensed"
#     tables2_pagination = 10
#     login_required=False
#     permission_required=False
#     ordering = '-created_date'
#     # inlineformset = ScreenshotInlineFormset
# 
#     custom_templates = {
#         'detail': 'applications/detail.html',
#     }
# 
#     @classmethod
#     def custom_context(cls, request, context, **kwargs):
#         """custom context"""
#         context['search_fields'] = ['type','name', 'status','features','environments']
#         context['extra_button'] = True
#         return context
# 
#     @classmethod
#     def custom_queryset(cls, request, **kwargs):
#         """custom queryset"""
#         d = request.GET
#         objects = Software.objects.all()
#         if ''.join([d[k] for k in d if k !='page' and k != 'sort']):
#             q_list = [Q(
#                     ("{}__icontains".format(k),d[k]))
#                     for k in d if k!='page' and d[k]!='' and k != 'sort']
#             objects = objects.filter(reduce(operator.or_, q_list))
#         return objects.order_by('-created_date')


class ProductCRUD(BaseCrudBuilder):
    """product crud"""
    model = Products
    search_fields = ['version', 'title','system','database','created_date','updated_date']
    tables2_fields = ('software','version', 'title','system','database',
                      'created_date','updated_date')
    tables2_css_class = "table table-bordered table-condensed"
    modelform_excludes = ('created_by','updated_by')
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
        return context

    # @classmethod
    # def custom_queryset(cls, request, **kwargs):
    #     """custom queryset"""
    #     id = request.GET.get('id',None)
    #     try:
    #         software = Software.objects.get(id=id)
    #         objects = Product.objects.filter(software=software)
    #     except Products.DoesNotExist as e:
    #         print("id is None fetch all products")
    #         objects = Product.objects.all()
    #     d = request.GET
    #     if ''.join([d[k] for k in d if k !='page' and k != 'sort' and k != 'id']):
    #         q_list = [Q(
    #                 ("{}__icontains".format(k),d[k]))
    #                 for k in d if k!='page' and d[k]!='' and k != 'sort' and k != 'id']
    #         objects = objects.filter(reduce(operator.or_, q_list))
    #     return objects.order_by('-created_date')