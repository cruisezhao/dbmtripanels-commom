'''
Created on Jun 30, 2017

@author: ben
'''
import django_filters
from .models import PACKAGE_STATUS, Packages
from django import forms
from datetimewidget.widgets import DateWidget
from common.utilities.utils import gen_choices
from django.db.models import Q
from django.utils.functional import lazy

class PackageFilter(django_filters.FilterSet):
    """package filter set"""
    id = django_filters.CharFilter(lookup_expr='exact', label='ID',
                                     widget = forms.TextInput(attrs={'class':'form-control'}),)
    package_name = django_filters.CharFilter(name='package_name', lookup_expr='icontains',label='Package Name',
                                             widget = forms.TextInput(attrs={'class':'form-control'}),)
    #if attribute name is email, html input label generated is readonly, so here email name is changed to email2
    email2 = django_filters.CharFilter(name='client__email', lookup_expr='icontains', label='email',
                                       widget = forms.TextInput(attrs={'class':'form-control'}),)
    start_date = django_filters.DateFilter(name='created', lookup_expr='gte',label='Start Date',
                                           widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    end_date = django_filters.DateFilter(name='created', lookup_expr='lte',label='End Date',
                                         widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    
    
    status = django_filters.MultipleChoiceFilter(choices=lazy(gen_choices,list)(Packages, 'status', PACKAGE_STATUS), 
                                                 widget=forms.CheckboxSelectMultiple())
    
    q = django_filters.CharFilter(
        method = 'search',
        label = 'Search',
    )
    
    def search(self, queryset, name, value):

        if not value.strip():
            return queryset
        qs_filter = (
            #Q(id__exact=value) |
            Q(package_name__icontains=value) |
            Q(client__email__icontains=value)
        )
        return queryset.filter(qs_filter)
    
    class Meta:
        model = Packages
        fields = ['q','status','id','package_name','email2','start_date','end_date',]


