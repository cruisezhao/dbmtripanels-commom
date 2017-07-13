from django import forms
from datetimewidget.widgets import DateWidget
from .models import SystemOptions
from common.apps.packages.models import Packages
from common.apps.deployments.models import DeployPolicies

class DeployForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #here must use pop method to delete extra parameter, or else __init__ will fail 
        self.package_id = kwargs.pop('package_id')
        super(DeployForm, self).__init__(*args, **kwargs)
        self.package = Packages.objects.get(uuid=self.package_id)
        order = self.package.get_product_order()
        self.plan = order.plan
        policy_set = DeployPolicies.objects.filter(product=order.product)
        if len(policy_set) == 0:
            policy = DeployPolicies.objects.get(plan=order.plan)
        else:
            policy = policy_set[0]
        #construct fields choices by varied deploy policy
        self.deploy_instance_list = policy.deployinstances_set.all()
        for ins in self.deploy_instance_list:
            groups = ins.get_options_by_type()
            for (option_type, sys_options) in groups.items():
                field_name = ins.uuid + '_' + option_type
                self.fields[field_name] = forms.ChoiceField(
                    choices=[(option.name, option.value) for option in sys_options ],
                    required=True,
                    
                )
    
    def deploy(self):
        #call infrastructure deploy API
        print('deploy starting...')
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
