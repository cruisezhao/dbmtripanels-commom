'''
Created on Jun 30, 2017

@author: ben
'''
import django_filters
from common.apps.orders.models import ORDER_STATUS, Orders

class OrderFilter(django_filters.FilterSet):
    """product filter set"""
    uuid = django_filters.CharFilter(lookup_expr='icontains', label='uuid')
    #if attribute name is email, html input label generated is readonly, so here email name is changed to email2
    email2 = django_filters.CharFilter(name='client__email', lookup_expr='icontains', label='email')
    created_date = django_filters.DateFromToRangeFilter(name='created_date')
    #end_date = django_filters.DateFilter(name='created_date', lookup_expr='gte')
    product_name = django_filters.CharFilter(name='product__product_name', lookup_expr='icontains')
    cpu_cores = django_filters.NumberFilter(name='plan__cpu', lookup_expr='exact')
    memory = django_filters.NumberFilter(name='plan__memory', lookup_expr='exact')
    disk = django_filters.NumberFilter(name='plan__disk', lookup_expr='exact')
    status = django_filters.MultipleChoiceFilter(choices=ORDER_STATUS)
    price = django_filters.NumberFilter(name='amount', lookup_expr='exact')
    
    class Meta:
        model = Orders
        fields = ['uuid','email2','created_date','product_name', 'cpu_cores','memory','disk','status','price']


