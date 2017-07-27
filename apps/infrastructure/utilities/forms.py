from __future__ import unicode_literals
import csv
import itertools
import re
from django import forms
from django.conf import settings
from django.core.validators import URLValidator
from django.urls import reverse_lazy


class SelectWithDisabled(forms.Select):
    """
    Modified the stock Select widget to accept choices using a dict() for a label. The dict for each option must include
    'label' (string) and 'disabled' (boolean).
    """
    option_template_name = 'selectwithdisabled_option.html'

class APISelect(SelectWithDisabled):
    """
    A select widget populated via an API call

    :param api_url: API URL
    :param display_field: (Optional) Field to display for child in selection list. Defaults to `name`.
    :param disabled_indicator: (Optional) Mark option as disabled if this field equates true.
    """

    def __init__(self, api_url, display_field=None, disabled_indicator=None, *args, **kwargs):

        super(APISelect, self).__init__(*args, **kwargs)

        self.attrs['class'] = 'api-select'
        self.attrs['api-url'] = '/{}{}'.format(settings.BASE_PATH, api_url.lstrip('/'))  # Inject BASE_PATH
        if display_field:
            self.attrs['display-field'] = display_field
        if disabled_indicator:
            self.attrs['disabled-indicator'] = disabled_indicator


class ChainedModelChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField which is initialized based on the values of other fields within a form. `chains` is a dictionary
    mapping of model fields to peer fields within the form. For example:

        country1 = forms.ModelChoiceField(queryset=Country.objects.all())
        city1 = ChainedModelChoiceField(queryset=City.objects.all(), chains={'country': 'country1'}

    The queryset of the `city1` field will be modified as

        .filter(country=<value>)

    where <value> is the value of the `country1` field. (Note: The form must inherit from ChainedFieldsMixin.)
    """
    def __init__(self, chains=None, *args, **kwargs):
        self.chains = chains
        super(ChainedModelChoiceField, self).__init__(*args, **kwargs)