from django import forms
from datetimewidget.widgets import DateWidget
from .models import SystemOptions


class SysOptionFilterForm(forms.Form):
    name = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class':'TinputText'}),
        label = 'name'
    )
    value = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class':'TinputText'}),
        label = 'value'
    )

    start_date = forms.DateField(
        required = False,
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        label = 'Start Date'
    )

    end_date = forms.DateField(
        required=False,
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        label='End Date'
        )


class SystemOptionForm(forms.ModelForm):
    class Meta:
        model = SystemOptions
        fields = ['type', 'name', 'value']