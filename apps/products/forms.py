from django.forms import ModelForm
from django.db.models import Count
from django import forms
from django.utils.html import mark_safe
from .models import Products, Plans
from common.utilities.extra_forms import CustomFieldFilterForm
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from common.utilities.forms import FilterChoiceField


class ProductForm(ModelForm):
    """product form"""

    class Meta:
        model = Products
        fields = ('product_type', 'product_name',)


def product_type_choice():
    """choice for product type"""
    pt_d = {}
    ps = Products.objects.values('product_type').annotate(count=Count('product_type'))
    for p in ps:
        pt_d[p['product_type']] = p['count']
    return [(t[0], mark_safe("{} <span class='badge pull-right'>{}</span>".format(t[1],pt_d.get(t[0],0)))) for t in Products.TYPE_CHOICE ]


class ProductFilterForm(forms.Form):
    """
        product filterform
    """
    q = forms.CharField(required=False, label='Search')

    name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={'class':'form-control'}),
        label='Name')

    plan = FilterChoiceField(
        queryset=Plans.objects.annotate(filter_count=Count('products')),
        widget=forms.CheckboxSelectMultiple(),
        to_field_name='pk',
    )

    type = forms.MultipleChoiceField(
        choices = product_type_choice,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    start_date = forms.DateField(
        required=False,
        label='Start_date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_date = forms.DateField(
        required=False,
        label='End_date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3
        ),
    )

    # class Meta:
    #     model = Products
    #     fields = ['q', 'name']