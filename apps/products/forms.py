from django.forms import ModelForm
from django import forms
from .models import Products
from common.utilities.extra_forms import CustomFieldFilterForm


class ProductForm(ModelForm):
    """product form"""

    class Meta:
        model = Products
        fields = ('product_type', 'product_name',)


class ProductFilterForm(forms.Form):
    """
        product filterform
    """
    q = forms.CharField(required=False, label='Search')


# class SoftwareShowForm(ModelForm):
#     """show software in portal"""
#     def __init__(self, *args, **kwargs):
#         super(SoftwareShowForm, self).__init__(*args,**kwargs)
#         self.fields['type'].widget.attrs['readonly'] = True
#         self.fields['name'].widget.attrs['readonly'] = True
#
#     class Meta:
#         model = Products
#         fields = ('type', 'name', 'in_homepage')