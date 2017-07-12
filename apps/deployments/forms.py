from django import forms
from datetimewidget.widgets import DateWidget
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)


from django import forms

class DeployForm(forms.Form):
    pass
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

class CloudForm(forms.ModelForm):
    class Meta:
        model = Clouds
        fields = ['name']


class DeployPolicyForm(forms.ModelForm):
    class Meta:
        model = DeployPolicies
        fields = ['plan', 'product',]
        # fields = ['relationships']


class DeployInstanceForm(forms.ModelForm):
    class Meta:
        model = DeployInstances
        fields = ['deploy_policy','cloud']

class InstanceConfigurationForm(forms.ModelForm):
    class Meta:
        model = InstanceConfigurations
        fields = ['deploy_instance','system_option']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['id','product','name','type','required']
