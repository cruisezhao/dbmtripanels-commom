from django.conf.urls import include,url
from .views4admin import SystemOptionListView

urlpatterns = [
    url(r'^sys-options/$', SystemOptionListView.as_view(), name='sys_option_list'),
    # url(r'^sys-options/(?P<uuid>[a-z\d+]{32})/$', SystemOption.as_view(), name='sys_option'),
    # url(r'^sys-options/add/$', SystemOptionEditView.as_view(), name='sys_option_add'),
    # url(r'^sys_options/(?P<uuid>[a-z\d+]{32}/edit/$', SystemOption.as_view(), name='sys_option_edit'),
    # url(r'^sys_options/(?P<uuid>[a-z\d+]{32}/delete/$', SystemOption.as_view(), name='sys_option_delete'),
]