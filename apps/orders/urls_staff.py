from django.conf.urls import url

from . import views
from . import views_new

urlpatterns = [
    #url(r'^list/$', views.list_orders, kwargs={}, name="list"),
    url(r'^list/$', views_new.OrderListView.as_view(), name='list'),
    url(r'^detail/(?P<uuid>\w+)/$', views.detail_orders, name='detail'),

]
