from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Products, Plans
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from common.utilities.views import (
    ObjectEditView, ObjectDeleteView, ObjectListView,BulkEditView, BulkDeleteView)
from . import forms
from . import filters
from . import tables


class ProductListView(ObjectListView):
    """product list"""
    queryset = Products.objects.all()
    filter = filters.ProductFilter
    filter_form = forms.ProductFilterForm
    table = tables.ProductTable
    template_name = 'products/product_list.html'


class ProductView(View):
    """product object view"""
    def get(self,request,uuid):
        product = get_object_or_404(Products,uuid=uuid)
        return render(request, "products/product.html", {'object':product})


class ProductEditView(ObjectEditView):
    """product edit"""
    model = Products
    form_class = forms.ProductForm
    template_name = 'products/product_edit.html'
    default_return_url = 'product_list'


class ProductDeleteView(ObjectDeleteView):
    model = Products
    default_return_url = 'product_list'


class ProductBulkDeleteView(BulkDeleteView):
    cls = Products
    filter = filters.ProductFilter
    default_return_url = 'product_list'


class ProductBulkEditView(BulkEditView):
    cls = Products
    filter = filters.ProductFilter
    form = forms.ProductBulkEditForm
    template_name = 'products/product_bulk_edit.html'
    default_return_url = 'product_list'


class PlanListView(ObjectListView):
    """plan list"""
    queryset = Plans.objects.all()
    filter = filters.PlanFilter
    filter_form = forms.PlanFilterForm
    table = tables.PlanTable
    template_name = 'products/plan_new_list.html'


class PlanView(View):
    """plan"""
    def get(self,request,uuid):
        plan = get_object_or_404(Plans,uuid=uuid)
        return render(request, "products/plan.html", {'object':plan})


class PlanEditView(ObjectEditView):
    """plan edit"""
    model = Plans
    form_class = forms.PlanForm
    template_name = 'products/plan_edit.html'
    default_return_url = 'plan_list'


class PlanDeleteView(ObjectDeleteView):
    """plan delete"""
    model = Plans
    default_return_url = 'plan_list'