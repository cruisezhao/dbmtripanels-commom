'''
Created on Jun 30, 2017

@author: ben
'''
import django_filters
from .models import ORDER_STATUS, Orders
from django import forms
from datetimewidget.widgets import DateWidget
from common.utilities.utils import gen_choices
from django.db.models import Q
from django.utils.functional import lazy

class OrderFilter(django_filters.FilterSet):
    """order filter set"""
    id = django_filters.CharFilter(lookup_expr='exact', label='ID',
                                     widget = forms.TextInput(attrs={'class':'form-control'}),)
    #if attribute name is email, html input label generated is readonly, so here email name is changed to email2
    email2 = django_filters.CharFilter(name='client__email', lookup_expr='icontains', label='Email',
                                       widget = forms.TextInput(attrs={'class':'form-control'}),)
    start_date = django_filters.DateFilter(name='created_date', lookup_expr='gte',label='Start Date',
                                           widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    end_date = django_filters.DateFilter(name='created_date', lookup_expr='lte', label='End Date',
                                         widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    product_name = django_filters.CharFilter(name='product__product_name', lookup_expr='icontains', label='Product Name',
                                             widget = forms.TextInput(attrs={'class':'form-control'}),)
    cpu_cores = django_filters.NumberFilter(name='plan__cpu', lookup_expr='exact')
    memory = django_filters.NumberFilter(name='plan__memory', lookup_expr='exact')
    disk = django_filters.NumberFilter(name='plan__disk', lookup_expr='exact')
    status = django_filters.MultipleChoiceFilter(choices=lazy(gen_choices,list)(Orders, 'status', ORDER_STATUS), 
                                                 widget=forms.CheckboxSelectMultiple())
    price = django_filters.NumberFilter(name='amount', lookup_expr='exact')
    
    q = django_filters.CharFilter(
        method = 'search',
        label = 'Search',
    )
    
    def search(self, queryset, name, value):

        if not value.strip():
            return queryset
        qs_filter = (
            #Q(id__exact=value) |
            Q(client__email__icontains=value) |
            Q(product__product_name__icontains=value)
        )
        return queryset.filter(qs_filter)
    
    class Meta:
        model = Orders
        fields = ['q','status','id','email2','start_date','end_date','product_name', 'cpu_cores','memory','disk','price']


