from django.conf.urls import url,include
from  .view4staff import (RackListView, RackView, RackEditView,RackDeleteView,
                          DataCenterListView, DataCenterView, DataCenterEditView, DataCenterDeleteView,
                          VendorListView, VendorView, VendorEditView, VendorDeleteView,
                          DevicePowerList,DevicePowerView,DevicePowerEditView,DevicePowerDeleteView,
                          DeviceDriveList, DeviceDriveView, DeviceDriveEditView, DeviceDriveDeleteView,
                          DeviceKVMList, DeviceKVMView, DeviceKVMEditView, DeviceKVMDeleteView,
                          DeviceRouterList,DeviceRouterView,DeviceRouterEditView,DeviceRouterDeleteView)


urlpatterns = [
    #vendors
    url(r'^vendors/$', VendorListView.as_view(), name='vendor_list'),
    url(r'^vendors/(?P<uuid>[a-z\d+]{32})/$', VendorView.as_view(), name='vendor'),
    url(r'^vendors/add/$', VendorEditView.as_view(), name='vendor_add'),
    url(r'^vendors/(?P<uuid>[a-z\d+]{32})/edit/$', VendorEditView.as_view(), name='vendor_edit'),
    url(r'^vendors/(?P<uuid>[a-z\d+]{32})/delete/$', VendorDeleteView.as_view(), name='vendor_delete'),

    #data center
    url(r'^data-centers/$', DataCenterListView.as_view(), name='data_center_list'),
    url(r'^data-centers/(?P<uuid>[a-z\d+]{32})/$', DataCenterView.as_view(), name='data_center'),
    url(r'^data-centers/add/$', DataCenterEditView.as_view(), name='data_center_add'),
    url(r'^data-centers/(?P<uuid>[a-z\d+]{32})/edit/$', DataCenterEditView.as_view(), name='data_center_edit'),
    url(r'^data-centers/(?P<uuid>[a-z\d+]{32})/delete/$', DataCenterDeleteView.as_view(), name='data_center_delete'),

    #rack
    url(r'^racks/$', RackListView.as_view(), name='rack_list'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/$', RackView.as_view(), name='rack'),
    url(r'^racks/add/$', RackEditView.as_view(), name='rack_add'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/edit/$', RackEditView.as_view(), name='rack_edit'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/delete/$', RackDeleteView.as_view(), name='rack_delete'),

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
]
