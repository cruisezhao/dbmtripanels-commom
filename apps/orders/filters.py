'''
Created on Jun 30, 2017

@author: ben
'''
import django_filters
from .models import ORDER_STATUS, Orders
from django import forms
from datetimewidget.widgets import DateWidget
from common.utilities.utils import gen_choices

class OrderFilter(django_filters.FilterSet):
    """order filter set"""
    uuid = django_filters.CharFilter(lookup_expr='icontains', label='uuid',
                                     widget = forms.TextInput(attrs={'class':'form-control'}),)
    #if attribute name is email, html input label generated is readonly, so here email name is changed to email2
    email2 = django_filters.CharFilter(name='client__email', lookup_expr='icontains', label='email',
                                       widget = forms.TextInput(attrs={'class':'form-control'}),)
    start_date = django_filters.DateFilter(name='created_date', lookup_expr='lte',
                                           widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    end_date = django_filters.DateFilter(name='created_date', lookup_expr='gte',
                                         widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    product_name = django_filters.CharFilter(name='product__product_name', lookup_expr='icontains',
                                             widget = forms.TextInput(attrs={'class':'form-control'}),)
    cpu_cores = django_filters.NumberFilter(name='plan__cpu', lookup_expr='exact')
    memory = django_filters.NumberFilter(name='plan__memory', lookup_expr='exact')
    disk = django_filters.NumberFilter(name='plan__disk', lookup_expr='exact')
    status = django_filters.MultipleChoiceFilter(choices=gen_choices(Orders, 'status', ORDER_STATUS), 
                                                 widget=forms.CheckboxSelectMultiple())
    price = django_filters.NumberFilter(name='amount', lookup_expr='exact')
    
    class Meta:
        model = Orders
        fields = ['uuid','email2','start_date','end_date','product_name', 'cpu_cores','memory','disk','status','price']


