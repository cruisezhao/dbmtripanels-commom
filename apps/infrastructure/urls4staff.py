from django.conf.urls import url,include
from  .view4staff import (RackListView, RackView, RackEditView,RackDeleteView,
                          DataCenterListView, DataCenterView, DataCenterEditView, DataCenterDeleteView,
                          VendorListView, VendorView, VendorEditView, VendorDeleteView,
                          DevicePowerList,DevicePowerView,DevicePowerEditView,DevicePowerDeleteView,
                          DeviceDriveList, DeviceDriveView, DeviceDriveEditView, DeviceDriveDeleteView,
                          DeviceKVMList, DeviceKVMView, DeviceKVMEditView, DeviceKVMDeleteView,
                          DeviceRouterList,DeviceRouterView,DeviceRouterEditView,DeviceRouterDeleteView,
                          DeviceSwitcheListView,DeviceSwitcheView,DeviceSwitcheEditView,DeviceSwitcheDeleteView,
                          DeviceFirewallListView, DeviceFirewallView, DeviceFirewallEditView,DeviceFirewallDeleteView,
                          DeviceBareListView,DeviceBareView,DeviceBareEditView,DeviceBareDeleteView,
                          DeviceMaintenanceListView,DeviceMaintenanceView,DeviceMaintenanceEditView,DeviceMaintenanceDeleteView,
                          InterfaceRackListView, InterfaceRackView, InterfaceRackEditView,InterfaceRackDeleteView,
                          InterfaceNetworkListView, InterfaceNetworkView,InterfaceNetworkEditView,InterfaceNetworkDeleteView,
                          ConnectionListView, ConnectionView, ConnectionEditView, ConnectionDeleteView,
                          #ip
                          VlanListView, VlanView, VlanEditView, VlanDeleteView,
                          IPPrefixListView, IPPrefixView, IPPrefixEditView, IPPrefixDeleteView,
                          IPAddressListView, IPAddressView, IPAddressEditView, IPAddressDeleteView,
                          ConnectionListView, ConnectionView, ConnectionEditView, ConnectionDeleteView,
                          # interfaceconnection_add,
                          InterfaceAddView)



urlpatterns = [
    #vendors
    url(r'^vendors/$', VendorListView.as_view(), name='vendor_list'),
    url(r'^vendors/(?P<id>[\d+])/$', VendorView.as_view(), name='vendor'),
    url(r'^vendors/add/$', VendorEditView.as_view(), name='vendor_add'),
    url(r'^vendors/(?P<id>[\d+])/edit/$', VendorEditView.as_view(), name='vendor_edit'),
    url(r'^vendors/(?P<id>[\d+])/delete/$', VendorDeleteView.as_view(), name='vendor_delete'),

    #data center
    url(r'^data-centers/$', DataCenterListView.as_view(), name='data_center_list'),
    url(r'^data-centers/(?P<id>[\d+])/$', DataCenterView.as_view(), name='data_center'),
    url(r'^data-centers/add/$', DataCenterEditView.as_view(), name='data_center_add'),
    url(r'^data-centers/(?P<id>[\d+])/edit/$', DataCenterEditView.as_view(), name='data_center_edit'),
    url(r'^data-centers/(?P<id>[\d+])/delete/$', DataCenterDeleteView.as_view(), name='data_center_delete'),

    #rack
    url(r'^racks/$', RackListView.as_view(), name='rack_list'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/$', RackView.as_view(), name='rack'),
    url(r'^racks/add/$', RackEditView.as_view(), name='rack_add'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/edit/$', RackEditView.as_view(), name='rack_edit'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/delete/$', RackDeleteView.as_view(), name='rack_delete'),
    # url(r'^racks/(?P<uuid>[a-z\d+]{32})/interface-connections/add/$', interfaceconnection_add, name='interfaceconnection_add'),

    #power
    url(r'^powers/$', DevicePowerList.as_view(), name='power_list'),
    url(r'^powers/(?P<uuid>[a-z\d+]{32})/$', DevicePowerView.as_view(), name='power'),
    url(r'^powers/add/$', DevicePowerEditView.as_view(), name='power_add'),
    url(r'^powers/(?P<uuid>[a-z\d+]{32})/edit/$', DevicePowerEditView.as_view(), name='power_edit'),
    url(r'^powers/(?P<uuid>[a-z\d+]{32})/delete/$', DevicePowerDeleteView.as_view(), name='power_delete'),

    #power
    url(r'^drivers/$', DeviceDriveList.as_view(), name='driver_list'),
    url(r'^drivers/(?P<uuid>[a-z\d+]{32})/$', DeviceDriveView.as_view(), name='driver'),
    url(r'^drivers/add/$', DeviceDriveEditView.as_view(), name='driver_add'),
    url(r'^drivers/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceDriveEditView.as_view(), name='driver_edit'),
    url(r'^drivers/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceDriveDeleteView.as_view(), name='driver_delete'),

    #DeviceKVMs
    url(r'^kvms/$', DeviceKVMList.as_view(), name='kvm_list'),
    url(r'^kvms/(?P<uuid>[a-z\d+]{32})/$', DeviceKVMView.as_view(), name='kvm'),
    url(r'^kvms/add/$', DeviceKVMEditView.as_view(), name='kvm_add'),
    url(r'^kvms/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceKVMEditView.as_view(), name='kvm_edit'),
    url(r'^kvms/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceKVMDeleteView.as_view(), name='kvm_delete'),

    #DeviceRouters
    url(r'^routers/$', DeviceRouterList.as_view(), name='router_list'),
    url(r'^routers/(?P<uuid>[a-z\d+]{32})/$', DeviceRouterView.as_view(), name='router'),
    url(r'^routers/add/$', DeviceRouterEditView.as_view(), name='router_add'),
    url(r'^routers/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceRouterEditView.as_view(), name='router_edit'),
    url(r'^routers/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceRouterDeleteView.as_view(), name='router_delete'),

    #DeviceSwitches
    url(r'^switches/$', DeviceSwitcheListView.as_view(), name='switch_list'),
    url(r'^switches/(?P<uuid>[a-z\d+]{32})/$', DeviceSwitcheView.as_view(), name='switch'),
    url(r'^switches/add/$', DeviceSwitcheEditView.as_view(), name='switch_add'),
    url(r'^switches/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceSwitcheEditView.as_view(), name='switch_edit'),
    url(r'^switches/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceSwitcheDeleteView.as_view(), name='switch_delete'),

    #DeviceFirewalls
    url(r'^firewalls/$', DeviceFirewallListView.as_view(), name='firewall_list'),
    url(r'^firewalls/(?P<uuid>[a-z\d+]{32})/$', DeviceFirewallView.as_view(), name='firewall'),
    url(r'^firewalls/add/$', DeviceFirewallEditView.as_view(), name='firewall_add'),
    url(r'^firewalls/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceFirewallEditView.as_view(), name='firewall_edit'),
    url(r'^firewalls/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceFirewallDeleteView.as_view(), name='firewall_delete'),

    #DeviceBares
    url(r'^bares/$', DeviceBareListView.as_view(), name='bare_list'),
    url(r'^bares/(?P<uuid>[a-z\d+]{32})/$', DeviceBareView.as_view(), name='bare'),
    url(r'^bares/add/$', DeviceBareEditView.as_view(), name='bare_add'),
    url(r'^bares/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceBareEditView.as_view(), name='bare_edit'),
    url(r'^bares/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceBareDeleteView.as_view(), name='bare_delete'),

    #DeviceMaintenances
    url(r'^device-maintenances/$', DeviceMaintenanceListView.as_view(), name='device_maintenance_list'),
    url(r'^device-maintenances/(?P<uuid>[a-z\d+]{32})/$', DeviceMaintenanceView.as_view(), name='device_maintenance'),
    url(r'^device-maintenances/add/$', DeviceMaintenanceEditView.as_view(), name='device_maintenance_add'),
    url(r'^device-maintenances/(?P<uuid>[a-z\d+]{32})/edit/$', DeviceMaintenanceEditView.as_view(), name='device_maintenance_edit'),
    url(r'^device-maintenances/(?P<uuid>[a-z\d+]{32})/delete/$', DeviceMaintenanceDeleteView.as_view(), name='device_maintenance_delete'),

    #InterfaceRacks
    url(r'^interface-racks/$', InterfaceRackListView.as_view(), name='interface_rack_list'),
    url(r'^interface-racks/(?P<uuid>[a-z\d+]{32})/$', InterfaceRackView.as_view(), name='interface_rack'),
    url(r'^interface-racks/add/$', InterfaceRackEditView.as_view(), name='interface_rack_add'),
    url(r'^interface-racks/(?P<uuid>[a-z\d+]{32})/edit/$', InterfaceRackEditView.as_view(), name='interface_rack_edit'),
    url(r'^interface-racks/(?P<uuid>[a-z\d+]{32})/delete/$', InterfaceRackDeleteView.as_view(), name='interface_rack_delete'),
    url(r'^devices/(?P<uuid>[a-z\d+]{32})/interfaces/add/$', InterfaceAddView.as_view(), name='interface_add'),

    #InterfaceNetworks
    url(r'^interface-networks/$', InterfaceNetworkListView.as_view(), name='interface_network_list'),
    url(r'^interface-networks/(?P<uuid>[a-z\d+]{32})/$', InterfaceNetworkView.as_view(), name='interface_network'),
    url(r'^interface-networks/add/$', InterfaceNetworkEditView.as_view(), name='interface_network_add'),
    url(r'^interface-networks/(?P<uuid>[a-z\d+]{32})/edit/$', InterfaceNetworkEditView.as_view(), name='interface_network_edit'),
    url(r'^interface-networks/(?P<uuid>[a-z\d+]{32})/delete/$', InterfaceNetworkDeleteView.as_view(), name='interface_network_delete'),

    #Connections
    url(r'^connections/$', ConnectionListView.as_view(), name='connection_list'),
    url(r'^connections/(?P<uuid>[a-z\d+]{32})/$', ConnectionView.as_view(), name='connection'),
    url(r'^connections/add/$', ConnectionEditView.as_view(), name='connection_add'),
    url(r'^connections/(?P<uuid>[a-z\d+]{32})/edit/$', ConnectionEditView.as_view(), name='connection_edit'),
    url(r'^connections/(?P<uuid>[a-z\d+]{32})/delete/$', ConnectionDeleteView.as_view(), name='connection_delete'),

    #vlan
    url(r'^vlans/$', VlanListView.as_view(), name='vlan_list'),
    url(r'^vlans/(?P<id>[\d+])/$', VlanView.as_view(), name='vlan'),
    url(r'^vlans/add/$', VlanEditView.as_view(), name='vlan_add'),
    url(r'^vlans/(?P<id>[\d+])/edit/$', VlanEditView.as_view(), name='vlan_edit'),
    url(r'^vlans/(?P<id>[\d+])/delete/$', VlanDeleteView.as_view(), name='vlan_delete'),

    #prefix
    url(r'^prefixs/$', IPPrefixListView.as_view(), name='prefix_list'),
    url(r'^prefixs/(?P<id>[\d+])/$', IPPrefixView.as_view(), name='prefix'),
    url(r'^prefixs/add/$', IPPrefixEditView.as_view(), name='prefix_add'),
    url(r'^prefixs/(?P<id>[\d+])/edit/$', IPPrefixEditView.as_view(), name='prefix_edit'),
    url(r'^prefixs/(?P<id>[\d+])/delete/$', IPPrefixDeleteView.as_view(), name='prefix_delete'),

    #ipaddress
    url(r'^ip-addresses/$', IPAddressListView.as_view(), name='ip_address_list'),
    url(r'^ip-addresses/(?P<id>[\d+])/$', IPAddressView.as_view(), name='ip_address'),
    url(r'^ip-addresses/add/$', IPAddressEditView.as_view(), name='ip_address_add'),
    url(r'^ip-addresses/(?P<id>[\d+])/edit/$', IPAddressEditView.as_view(), name='ip_address_edit'),
    url(r'^ip-addresses/(?P<id>[\d+])/delete/$', IPAddressDeleteView.as_view(), name='ip_address_delete'),
]
