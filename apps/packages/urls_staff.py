from django.conf.urls import url

from . import views


urlpatterns = [
    #url(r'^list/$', views.list_orders, kwargs={}, name="list"),
    url(r'^list/$', views.PackageListView.as_view(), name='list'),
    url(r'^detail/(?P<uuid>\w+)/$', views.PackageView.as_view(), name='detail'),
    url(r'^edit/(?P<uuid>\w+)/$', views.PackageEditView.as_view(), name='edit'),
]
