from common.utilities.views import (ObjectListView, ObjectEditView,
                                    ObjectDeleteView)
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models.network import (DeviceRacks,DataCenters,Vendors,InterfaceRacks,
                                DevicePowers, DeviceDrives,DeviceKVMs,DeviceMaintenances,
                                DeviceRouters,DeviceSwitches, DeviceFirewalls,DeviceBares,
                                InterfaceNetworks,Connections)

from .models.ip import VLANs, IPPrefixes, IPAddresses, IPInterfaces
from . import filters
from . import forms
from . import tables
from .views import InterfaceCreateView
from common.utilities.views import TriPanelsBaseDetailView


class BaseDeviceDetailView(TriPanelsBaseDetailView):
    def get(self,request,uuid):
        obj = get_object_or_404(self.model,uuid=uuid)
        return render(request, self.template_name, {'object':obj, 'detail_exclude':self.detail_exclude, 'groups':self.Groups.groups, 'fields':self.fields})
    

class VendorListView(ObjectListView):
    queryset = Vendors.objects.all()
    filter = filters.VendorFilter
    filter_form = None
    table = tables.VerdorTable
    template_name = "vendors/vendor_list.html"


class VendorView(View):
    def get(self,request, id):
        vendor = get_object_or_404(Vendors, id=id)
        return render(request, 'vendors/vendor.html',{
            'object':vendor,
            'detail_exclude':['id','created_date','created_by',
                'updated_date','updated_by','username','password'],
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
    def get(self,request,id):
        datacenter = get_object_or_404(DataCenters, id=id)
        return render(request, "datacenters/datacenter.html",{
            'object':datacenter,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
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
    queryset = DeviceRacks.objects.select_related('devices_ptr')
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
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by','username','password'],
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
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
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
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceDriveEditView(ObjectEditView):
    model = DeviceDrives
    form_class = forms.DeviceDriveForm
    template_name = "drivers/drive_edit.html"
    default_return_url = "infras:driver_list"


class DeviceDriveDeleteView(ObjectDeleteView):
    model = DeviceDrives
    default_return_url = "infras:driver_list"


class DeviceKVMList(ObjectListView):
    queryset = DeviceKVMs.objects.all()
    filter = filters.DeviceKVMFilter
    filter_form = None
    table = tables.DeviceKVMTable
    template_name = "kvms/kvm_list.html"


class DeviceKVMView(View):
    def get(self,request,uuid):
        KVM = get_object_or_404(DeviceKVMs, uuid=uuid)
        return render(request, "kvms/kvm.html",{
            'object':KVM,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceKVMEditView(ObjectEditView):
    model = DeviceKVMs
    form_class = forms.DeviceKVMForm
    template_name = "kvms/kvm_edit.html"
    default_return_url = "infras:kvm_list"


class DeviceKVMDeleteView(ObjectDeleteView):
    model = DeviceKVMs
    default_return_url = "infras:kvm_list"


class DeviceRouterList(ObjectListView):
    queryset = DeviceRouters.objects.all()
    filter = filters.DeviceRouterFilter
    filter_form = None
    table = tables.DeviceRouterTable
    template_name = "routers/router_list.html"

class DeviceRouterView(View):

    def get(self,request,uuid):
        router = get_object_or_404(DeviceRouters, uuid=uuid)
        return render(request, "routers/router.html",{
            'object':router,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceRouterEditView(ObjectEditView):
    model = DeviceRouters
    default_return_url = "infras:router_list"
    form_class = forms.DeviceRouterForm
    template_name = "routers/router_edit.html"


class DeviceRouterDeleteView(ObjectDeleteView):
    model = DeviceRouters
    default_return_url = "infras:router_list"


class DeviceSwitcheListView(ObjectListView):
    queryset = DeviceSwitches.objects.all()
    filter = filters.DeviceSwitcheFilter
    filter_form = None
    table = tables.DeviceSwitcheTable
    template_name = "switches/switche_list.html"


class DeviceSwitcheView(View):
    def get(self,request,uuid):
        switche = get_object_or_404(DeviceSwitches, uuid=uuid)
        return render(request, "switches/switche.html",{
            'object':switche,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceSwitcheEditView(ObjectEditView):
    model = DeviceSwitches
    default_return_url = "infras:switche_list"
    template_name = "switches/switche_edit.html"
    form_class = forms.DeviceSwitcheForm


class DeviceSwitcheDeleteView(ObjectDeleteView):
    model = DeviceSwitches
    default_return_url = "infras:switche_list"


class DeviceFirewallListView(ObjectListView):
    queryset = DeviceFirewalls.objects.all()
    filter = filters.DeviceFirewallFilter
    filter_form = None
    table = tables.DeviceFirewallTable
    template_name = "firewalls/firewall_list.html"


class DeviceFirewallView(View):
    def get(self,request,uuid):
        firewall = get_object_or_404(DeviceFirewalls, uuid=uuid)
        return render(request, "firewalls/firewall.html",{
            'object':firewall,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceFirewallEditView(ObjectEditView):
    model = DeviceFirewalls
    default_return_url = "infras:firewall_list"
    form_class = forms.DeviceFirewallForm
    template_name = "firewalls/firewall_edit.html"


class DeviceFirewallDeleteView(ObjectDeleteView):
    model = DeviceFirewalls
    default_return_url = "infras:firewall_list"


class DeviceBareListView(ObjectListView):
    queryset = DeviceBares.objects.all()
    filter = filters.DeviceBareFilter
    filter_form = None
    table = tables.DeviceBareTable
    template_name = "bares/bare_list.html"


class DeviceBareView(View):
    def get(self,request,uuid):
        bare = get_object_or_404(DeviceBares, uuid=uuid)
        return render(request, "bares/bare.html",{
            'object':bare,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class DeviceBareEditView(ObjectEditView):
    model = DeviceBares
    default_return_url = "infras:bare_list"
    form_class = forms.DeviceBareForm
    template_name = "bares/bare_edit.html"


class DeviceBareDeleteView(ObjectDeleteView):
    model = DeviceBares
    default_return_url = "infras:bare_list"


class DeviceMaintenanceListView(ObjectListView):
    queryset = DeviceMaintenances.objects.all()
    filter = filters.DeviceMaintenanceFilter
    filter_form = None
    table = tables.DeviceMaintenanceTable
    template_name = "maintenances/maintenace_list.html"


class DeviceMaintenanceView(View):
    def get(self,request,uuid):
        maintenace = get_object_or_404(DeviceMaintenances, uuid=uuid)
        return render(request, "maintenances/maintenace.html",{
            "object":maintenace,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class InterfaceRackListView(ObjectListView):
    queryset = InterfaceRacks.objects.all()
    filter = filters.InterfaceRackFilter
    filter_form = None
    table = tables.InterfaceRackTable
    template_name = "interfaces/interface_rack_list.html"


class InterfaceRackView(View):
    def get(self,request,uuid):
        Irack = get_object_or_404(InterfaceRacks, uuid=uuid)
        return render(request, "interfaces/interface_rack.html",{
            "object":Irack,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class InterfaceRackEditView(ObjectEditView):
    model = InterfaceRacks
    default_return_url = "infras:interface_rack_list"
    form_class = forms.InterfaceRackForm
    template_name = "interfaces/interface_rack_edit.html"


class InterfaceRackDeleteView(ObjectDeleteView):
    model = InterfaceRacks
    default_return_url = "infras:interface_rack_list"

class DeviceMaintenanceEditView(ObjectEditView):
    model = DeviceMaintenances
    default_return_url = "infras:device_maintenance_list"
    form_class = forms.DeviceMaintenanceForm
    template_name = "maintenances/maintenace_edit.html"


class DeviceMaintenanceDeleteView(ObjectDeleteView):
    model = DeviceMaintenances
    default_return_url = "infras:device_maintenance_list"


class InterfaceNetworkListView(ObjectListView):
    queryset = InterfaceNetworks.objects.all()
    filter = filters.InterfaceNetworkFilter
    filter_form = None
    table = tables.InterfaceNetworkTable
    template_name = "interfaces/interface_network_list.html"


class InterfaceNetworkView(View):
    def get(self,request,uuid):
        network = get_object_or_404(InterfaceNetworks, uuid=uuid)
        return render(request, "interfaces/interface_network.html",{
            "object":network,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class InterfaceNetworkEditView(ObjectEditView):
    model = InterfaceNetworks
    default_return_url = "infras:interface_network_list"
    template_name = "interfaces/interface_network_edit.html"
    form_class = forms.InterfaceNetworkForm


class InterfaceNetworkDeleteView(ObjectDeleteView):
    model = InterfaceNetworks
    default_return_url = "infras:interface_network_list"


# def interfaceconnection_add(request, pk):
#     device = get_object_or_404(Devices, pk=pk)
#
#     if request.method == 'POST':
#         form = forms.InterfaceConnectionForm(device, request.POST)
#         if form.is_valid():
#
#             interfaceconnection = form.save()
#
#             if '_addanother' in request.POST:
#                 base_url = reverse('dcim:interfaceconnection_add', kwargs={'pk': device.pk})
#                 device_b = interfaceconnection.interface_b.device
#                 params = urlencode({
#                     'rack_b': device_b.rack.pk if device_b.rack else '',
#                     'device_b': device_b.pk,
#                 })
#                 return HttpResponseRedirect('{}?{}'.format(base_url, params))
#             else:
#                 return redirect('dcim:device', pk=device.pk)
#
#     else:
#         form = forms.InterfaceConnectionForm(device, initial={
#             'interface_a': request.GET.get('interface_a'),
#             'site_b': request.GET.get('site_b'),
#             'rack_b': request.GET.get('rack_b'),
#             'device_b': request.GET.get('device_b'),
#             'interface_b': request.GET.get('interface_b'),
#         })
#
#     return render(request, 'dcim/interfaceconnection_edit.html', {
#         'device': device,
#         'form': form,
#         'return_url': reverse('dcim:device', kwargs={'pk': device.pk}),
#     })

class InterfaceAddView(InterfaceCreateView):
    parent_model = DeviceRacks
    parent_field = 'device'
    model = InterfaceRacks
    form = forms.InterfaceCreateForm
    template_name = 'interfaces/interface_add.html'


class ConnectionListView(ObjectListView):
    queryset = Connections.objects.all()
    filter = filters.ConnectionFilter
    filter_form = None
    table = tables.ConnectionTable
    template_name = "interfaces/connection_list.html"


class ConnectionView(View):
    def get(self,request,uuid):
        connection = get_object_or_404(Connections, uuid=uuid)
        return render(request, "interfaces/connection.html",{
            "object":connection,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class ConnectionEditView(ObjectEditView):
    model = Connections
    default_return_url = "infras:connection_list"
    form_class = forms.ConnectionForm
    template_name = "interfaces/connection_edit.html"


class ConnectionDeleteView(ObjectDeleteView):
    model = Connections
    default_return_url = "infras:connection_list"


class VlanListView(ObjectListView):
    queryset = VLANs.objects.all()
    filter = filters.VlanFilter
    filter_form = None
    table = tables.VlanTable
    template_name = "ips/vlan_list.html"


class VlanView(View):
    def get(self,request, id):
        vlan = get_object_or_404(VLANs,id=id)
        return render(request, "ips/vlan.html",{
            "object":vlan,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class VlanEditView(ObjectEditView):
    model = VLANs
    default_return_url = "infras:vlan_list"
    form_class = forms.VlanForm
    template_name = "ips/vlan_edit.html"


class VlanDeleteView(ObjectDeleteView):
    model = VLANs
    default_return_url = "infras:vlan_list"


class IPPrefixListView(ObjectListView):
    queryset = IPPrefixes.objects.all()
    filter = filters.IPPrefixFilter
    filter_form = None
    table = tables.IPPrefixTable
    template_name = "ips/ip_prefix_list.html"


class IPPrefixView(View):
    def get(self,request, id):
        prefix = get_object_or_404(IPPrefixes,id=id)
        return render(request, "ips/ip_prefix.html",{
            "object":prefix,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class IPPrefixEditView(ObjectEditView):
    model = IPPrefixes
    default_return_url = "infras:prefix_list"
    form_class = forms.IPPrefixForm
    template_name = "ips/ip_prefix_edit.html"


class IPPrefixDeleteView(ObjectDeleteView):
    model = IPPrefixes
    default_return_url = "infras:prefix_list"


class IPAddressListView(ObjectListView):
    queryset = IPAddresses.objects.all()
    filter = filters.IPAddressFilter
    filter_form = None
    table = tables.IPAddressTable
    template_name = "ips/ip_address_list.html"


class IPAddressView(ObjectListView):
    def get(self, request, id):
        address = get_object_or_404(IPAddresses,id=id)
        return render(request, "ips/ip_address.html",{
            "object":address,
            'detail_exclude':['id','uuid','created_date','created_by',
                'updated_date','updated_by',],
        })


class IPAddressEditView(ObjectEditView):
    model = IPAddresses
    default_return_url = "infras:ip_address_list"
    form_class = forms.IPAddressForm
    template_name = "ips/ip_address_edit.html"


class IPAddressDeleteView(ObjectDeleteView):
    model = IPAddresses
    default_return_url = "infras:ip_address_list"