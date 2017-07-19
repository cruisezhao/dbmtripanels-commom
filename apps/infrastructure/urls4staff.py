from django.conf.urls import url,include
from  .view4staff import (RackListView, RackView, RackEditView,RackDeleteView)


urlpatterns = [
    #rack
    url(r'^racks/$', RackListView.as_view(), name='rack_list'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/$', RackView.as_view(), name='rack'),
    url(r'^racks/add/$', RackEditView.as_view(), name='rack_add'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/edit/$', RackEditView.as_view(), name='rack_edit'),
    url(r'^racks/(?P<uuid>[a-z\d+]{32})/delete/$', RackDeleteView.as_view(), name='rack_delete'),
]
