from __future__ import unicode_literals
import csv
import itertools
import re
from django import forms
from django.conf import settings
from django.core.validators import URLValidator
from django.urls import reverse_lazy

NUMERIC_EXPANSION_PATTERN = '\[((?:\d+[?:,-])+\d+)\]'

def parse_numeric_range(string, base=10):
    """
    Expand a numeric range (continuous or not) into a decimal or
    hexadecimal list, as specified by the base parameter
      '0-3,5' => [0, 1, 2, 3, 5]
      '2,8-b,d,f' => [2, 8, 9, a, b, d, f]
    """
    values = list()
    for dash_range in string.split(','):
        try:
            begin, end = dash_range.split('-')
        except ValueError:
            begin, end = dash_range, dash_range
        begin, end = int(begin.strip(), base=base), int(end.strip(), base=base) + 1
        values.extend(range(begin, end))
    return list(set(values))

def expand_numeric_pattern(string):
    """
    Expand a numeric pattern into a list of strings. Examples:
      'ge-0/0/[0-3,5]' => ['ge-0/0/0', 'ge-0/0/1', 'ge-0/0/2', 'ge-0/0/3', 'ge-0/0/5']
      'xe-0/[0,2-3]/[0-7]' => ['xe-0/0/0', 'xe-0/0/1', 'xe-0/0/2', ... 'xe-0/3/5', 'xe-0/3/6', 'xe-0/3/7']
    """
    lead, pattern, remnant = re.split(NUMERIC_EXPANSION_PATTERN, string, maxsplit=1)
    parsed_range = parse_numeric_range(pattern)
    for i in parsed_range:
        if re.search(NUMERIC_EXPANSION_PATTERN, remnant):
            for string in expand_numeric_pattern(remnant):
                yield "{}{}{}".format(lead, i, string)
        else:
            yield "{}{}{}".format(lead, i, remnant)

class ExpandableNameField(forms.CharField):
    """
    A field which allows for numeric range expansion
      Example: 'Gi0/[1-3]' => ['Gi0/1', 'Gi0/2', 'Gi0/3']
    """
    def __init__(self, *args, **kwargs):
        super(ExpandableNameField, self).__init__(*args, **kwargs)
        if not self.help_text:
            self.help_text = 'Numeric ranges are supported for bulk creation.<br />'\
                             'Example: <code>ge-0/0/[0-23,25,30]</code>'

    def to_python(self, value):
        if re.search(NUMERIC_EXPANSION_PATTERN, value):
            return list(expand_numeric_pattern(value))
        return [value]


class DeviceComponentForm(forms.Form):
    """
    Allow inclusion of the parent device as context for limiting field choices.
    """
    def __init__(self, device, *args, **kwargs):
        self.device = device
        super(DeviceComponentForm, self).__init__(*args, **kwargs)


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