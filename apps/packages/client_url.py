from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^productlist/$', views.list_user_products, kwargs={}, name="productlist"),
    url(r'^productdetails/(?P<pid>\w+)/$', views.product_details, kwargs={}, name="productdetails"),

]