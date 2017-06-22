from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.list_orders, kwargs={}, name="list"),
    url(r'^detail/(?P<uuid>\w+)/$', views.detail_orders, name='detail'),

]
