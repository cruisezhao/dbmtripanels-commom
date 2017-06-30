from django.forms import ModelForm
from django import forms
from .models import Products
from common.utilities.extra_forms import CustomFieldFilterForm
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget


class ProductForm(ModelForm):
    """product form"""

    class Meta:
        model = Products
        fields = ('product_type', 'product_name',)


class ProductFilterForm(ModelForm):
    """
        product filterform
    """
    q = forms.CharField(required=False, label='Search')
    name = forms.CharField(required=False, label='Name')
    start_date = forms.DateField(
        required=False,
        label='start_date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_date = forms.DateField(
        required=False,
        label='end_date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3
        ),
    )

    class Meta:
        model = Products
        fields = ['q', 'name']