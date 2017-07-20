from django.conf.urls import url,include
from  .view4staff import (RackListView, RackView, RackEditView,RackDeleteView,
                          DataCenterListView, DataCenterView, DataCenterEditView, DataCenterDeleteView,
                          VendorListView, VendorView, VendorEditView, VendorDeleteView,
                          DevicePowerList,DevicePowerView,DevicePowerEditView,DevicePowerDeleteView)


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
]
