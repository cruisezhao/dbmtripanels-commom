'''
Created on Jul 5, 2017

@author: ben
'''

'''
Created on Jun 30, 2017

@author: ben
'''
import django_filters
from .models import PACKAGE_STATUS, Packages
from django import forms
from datetimewidget.widgets import DateWidget
from common.utilities.utils import gen_choices

class PackageFilter(django_filters.FilterSet):
    """package filter set"""
    uuid = django_filters.CharFilter(lookup_expr='icontains', label='uuid',
                                     widget = forms.TextInput(attrs={'class':'form-control'}),)
    package_name = django_filters.CharFilter(name='package_name', lookup_expr='icontains',
                                             widget = forms.TextInput(attrs={'class':'form-control'}),)
    #if attribute name is email, html input label generated is readonly, so here email name is changed to email2
    email2 = django_filters.CharFilter(name='client__email', lookup_expr='icontains', label='email',
                                       widget = forms.TextInput(attrs={'class':'form-control'}),)
    start_date = django_filters.DateFilter(name='created', lookup_expr='lte',
                                           widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    end_date = django_filters.DateFilter(name='created', lookup_expr='gte',
                                         widget=DateWidget(
                                            options={'format': 'yyyy-mm-dd',},
                                            bootstrap_version=3),)
    
    
    status = django_filters.MultipleChoiceFilter(choices=gen_choices(Packages, 'status', PACKAGE_STATUS), 
                                                 widget=forms.CheckboxSelectMultiple())
    
    
    class Meta:
        model = Packages
        fields = ['uuid','package_name','email2','start_date','end_date','status']


