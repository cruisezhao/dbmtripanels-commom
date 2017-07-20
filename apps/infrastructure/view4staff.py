from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from common.utilities.views import (ObjectListView, ObjectEditView,
                            ObjectDeleteView)
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)
from . import filters
from . import tables
from . import forms


class VendorListView(ObjectListView):
    queryset = Vendors.objects.all()
    filter = filters.VendorFilter
    filter_form = None
    table = tables.VerdorTable
    template_name = "vendors/vendor_list.html"


class VendorView(View):
    def get(self,request, uuid):
        vendor = get_object_or_404(Vendors, uuid=uuid)
        return render(request, 'vendors/vendor.html',{
            'object':vendor,
        })


class VendorEditView(ObjectEditView):
    model = Vendors
    form_class = forms.VendorForm
    template_name = "vendors/vendor_edit.html"
    default_return_url = "infras:vendor_list"


class VendorDeleteView(ObjectDeleteView):
    model = Vendors
    default_return_url = "infras:vendor_list"


class DataCenterListView(ObjectListView):
    queryset = DataCenters.objects.all()
    filter = filters.DataCenterFilter
    filter_form = None
    table = tables.DataCenterTable
    template_name = "datacenters/datacenter_list.html"


class DataCenterView(View):
    def get(self,request,uuid):
        datacenter = get_object_or_404(DataCenters, uuid=uuid)
        return render(request, "datacenters/datacenter.html",{
            'object':datacenter,
        })


class DataCenterEditView(ObjectEditView):
    model = DataCenters
    form_class = forms.DataCentersForm
    template_name = "datacenters/datacenter_edit.html"
    default_return_url = "infras:data_center_list"


class DataCenterDeleteView(ObjectDeleteView):
    model = DataCenters
    default_return_url = "infras:data_center_list"


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


class DevicePowerList(ObjectListView):
    queryset = DevicePowers.objects.all()
    filter = filters.DevicePowerFilter
    filter_form = None
    table = tables.DevicePowerTable
    template_name = "powers/power_list.html"


class DevicePowerView(View):
    def get(self, request, uuid):
        power = get_object_or_404(DevicePowers, uuid = uuid)
        return render(request,"powers/power.html",{
            "object":power,
        })


class DevicePowerEditView(ObjectEditView):
    model = DevicePowers
    form_class = forms.DevicePowerForm
    template_name = "powers/power_edit.html"
    default_return_url = "infras:power_list"


class DevicePowerDeleteView(ObjectDeleteView):
    model = DevicePowers
    default_return_url = "infras:power_list"


class DeviceDriveList(ObjectListView):
    queryset = DeviceDrives.objects.all()
    filter = filters.DeviceDriveFilter
    form_class = None
    table = tables.DeviceDriveTable
    template_name = "drivers/driver_list.html"


class DeviceDriveView(View):
    def get(self,request,uuid):
        drive = get_object_or_404(DeviceDrives, uuid=uuid)
        return render(request, "drivers/drive.html",{
            'object':drive,
        })


class DeviceDriveEditView(ObjectEditView):
    model = DeviceDrives
    form_class = forms.DeviceDriveForm
    template_name = "drivers/drive_edit.html"
    default_return_url = "infras:driver_list"


class DeviceDriveDeleteView(ObjectDeleteView):
    model = DeviceDrives
    default_return_url = "infras:driver_list"