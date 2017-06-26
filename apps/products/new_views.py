from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Products
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from common.utilities.views import ObjectEditView, ObjectDeleteView
from . import forms


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
    default_return_url = 'home'


class ProductDeleteView(ObjectDeleteView):
    model = Products
    default_return_url = 'home'


