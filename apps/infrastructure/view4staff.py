from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from common.utilities.views import (ObjectListView, ObjectEditView,
                            ObjectDeleteView)
from .models.network import DeviceRacks
from . import filters
from . import tables
from . import forms

class RackListView(ObjectListView):
    queryset = DeviceRacks.objects.all()
    filter = filters.RackFilter
    filter_form = None
    table = tables.RackTable
    template_name = "racks/racks_list.html"


class RackView(View):
    """rack view"""
    def get(self,request,uuid):
        rack = get_object_or_404(DeviceRacks, uuid = uuid)
        return render(request, "racks/rack.html",{
            'object':rack,
        })


class RackEditView(ObjectEditView):
    model = DeviceRacks
    form_class = forms.DeviceRacksForm
    template_name = "racks/rack_edit.html"
    default_return_url ="infras:rack_list"


class RackDeleteView(ObjectDeleteView):
    model = DeviceRacks
    default_return_url = "infras:rack_list"
