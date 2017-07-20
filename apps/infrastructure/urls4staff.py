from django.conf.urls import url,include
from  .view4staff import (RackListView, RackView, RackEditView,RackDeleteView,
                          DataCenterListView, DataCenterView, DataCenterEditView, DataCenterDeleteView)


urlpatterns = [
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
]
