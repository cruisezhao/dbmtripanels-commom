from django.views.generic import View
from django.shortcuts import get_object_or_404, render
from common.utilities.views import ObjectEditView, ObjectDeleteView, ObjectListView
from . import forms
from . import filters
from . import tables
from .models import Clients


class ClientListView(ObjectListView):
    """client list"""
    queryset = Clients.objects.all()
    filter = filters.ClientFilter
    filter_form = forms.ClientFilterForm
    table = tables.ClientTable
    template_name = 'clients/client_list.html'


# class ClientDetailView(View):
#     """product object view"""
#     def get(self,request,uuid):
#         client = get_object_or_404(Clients,uuid=uuid)
#         return render(request, "products/product.html", {'object':product})
#
#
# class ClientEditView(ObjectEditView):
#     """product edit"""
#     model = Clients
#     form_class = forms.ClientForm
#     template_name = 'products/product_edit.html'
#     default_return_url = 'home'
#
#
# class ClientDeleteView(ObjectDeleteView):
#     model = Clients
#     default_return_url = 'home'