from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.list_user_order, kwargs={}, name="list"),
    #url(r'^detail/(?P<id>\w+)/$', views.detail_orders, name='detail'),
    url(r'^(?P<pro>[a-z\d]{32})/$', views.OrderCreateView.as_view(), name="req"),
    url(r'^notallow/$', views.OrderNotallowView.as_view(),),
    url(r'^success/$', views.OrderSuccess.as_view(), name="success"),

]