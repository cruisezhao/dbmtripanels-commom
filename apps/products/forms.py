import random
from django.forms import ModelForm
from django.db.models import Count
from django import forms
from django.utils.html import mark_safe
from .models import Products, Plans
from common.utilities.extra_forms import CustomFieldFilterForm
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from common.utilities.forms import FilterChoiceField, DateFilterMixin


class ProductForm(ModelForm):
    """product form"""

    class Meta:
        model = Products
        fields = ('product_type', 'product_name',)


class ProductBulkEditForm(forms.Form):
    def __init__(self,model,*args,**kwargs):
        super(ProductBulkEditForm,self).__init__(*args,**kwargs)
    pk = forms.ModelMultipleChoiceField(queryset=Products.objects.all(), widget=forms.MultipleHiddenInput)


def product_type_choice():
    """choice for product type"""
    pt_d = {}
    ps = Products.objects.values('product_type').annotate(count=Count('product_type'))
    for p in ps:
        pt_d[p['product_type']] = p['count']
    return [(t[0], mark_safe("{} <span class='badge pull-right'>{}</span>".format(t[1],pt_d.get(t[0],0)))) for t in Products.TYPE_CHOICE ]

def generic_choice(m, field, choice):
    """generic choice field
    @m the model
    @field to choice
    @choice is the checkbox
    """
    pt_d = {}
    ps = m.objects.values(field).annotate(count=Count(field))
    for p in ps:
        pt_d[p[field]] = p['count']
    return [(t[0], mark_safe("{} <span class='badge pull-right'>{}</span>".format(t[1],pt_d.get(t[0],0)))) for t in choice ]

class ProductFilterForm(forms.Form):
    """
        product filterform
    """
    type = forms.MultipleChoiceField(
        choices = product_type_choice,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="By Type",
    )
    plan = FilterChoiceField(
        queryset=Plans.objects.annotate(filter_count=Count('products')),
        widget=forms.CheckboxSelectMultiple(),
        to_field_name='pk',
        label="By Plan",
    )

    #q = forms.CharField(required=False, label='Search')

    name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={'class':'TinputText'}),
        label='Product Name',
        )

    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3
        ),
    )

    # class Meta:
    #     model = Products
    #     fields = ['q', 'name']


class PlanForm(ModelForm):
    class Meta:
        model = Plans
        fields = ('name', 'cpu','memory','disk','instance','price')


class PlanFilterForm(DateFilterMixin, forms.Form):
    """plan filter"""
    # cpu = forms.MultipleChoiceField(
    #     choices = generic_choice(
    #         Plans,
    #         'cpu',
    #         [(i,'{} cores'.format(i)) for i in range(4)]
    #                       ),
    #     widget = forms.CheckboxSelectMultiple(),
    #     required = False,
    #     label = "By CPU"
    # )
    #
    # memory = forms.MultipleChoiceField(
    #     choices = generic_choice(
    #         Plans,
    #         'memory',
    #         [(i,'{}GB'.format(i)) for i in range(8)]
    #     ),
    #     widget = forms.CheckboxSelectMultiple(),
    #     required = False,
    #     label = 'By Memory',
    # )
    #
    # disk = forms.MultipleChoiceField(
    #     choices = generic_choice(Plans,
    #                              'disk',
    #                              [(i,'{}disks'.format(i)) for i in range(4)]
    #                              ),
    #     widget = forms.CheckboxSelectMultiple(),
    #     required = False,
    #     label = 'By Disk'
    # )
    #
    # instance = forms.MultipleChoiceField(
    #     choices = generic_choice(Plans,
    #                              'instance',
    #                               [(i,'{}instance'.format(i)) for i in range(3)]
    # ),
    #     widget = forms.CheckboxSelectMultiple(),
    #     required = False,
    #     label = 'By Instance',
    # )
    #
    # price = forms.MultipleChoiceField(
    #     choices = generic_choice(Plans,
    #                              'price',
    #                              [(i,'{}$'.format(i)) for i in Plans.CHOICE]
    #                              ),
    #     widget = forms.CheckboxSelectMultiple(),
    #     required = False,
    #     label = 'By price'
    # )

    name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={'class':'TinputText'}),
        label='Plan Name',
        )