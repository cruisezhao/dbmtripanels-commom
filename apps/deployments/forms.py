from django import forms
from datetimewidget.widgets import DateWidget
from common.apps.packages.models import Packages
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)
from common.apps.deployments import apis
from common.apps.deployments.apis import make_callback
from common.apps.deployments.manager import DeployTaskManager



class DeployForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #here must use pop method to delete extra parameter, or else __init__ will fail 
        self.package_uuid = kwargs.pop('package_id')
        super(DeployForm, self).__init__(*args, **kwargs)
        self.package = Packages.objects.get(uuid=self.package_uuid)
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
        '''
        input parameter:
{
    "product_name":"Magento",
    "servers":[ {
        "cloud":cloud,
        "cpu": 2,
        "memory": 20,
        "disk": 200,
        "server_configurations":[system_option1,system_option2]
    }],
    "answers": {
        "cloud": "tripanels",
        "proxy_scheme": "https"
    }
}
    return:
        deploy_id
        '''
        if not self.package.allow_to_deploy():
            print('this package is deploying or deployed')
            return 'This package is deploying or deployed.'
        if DeployTaskManager.is_not_deploying_and_set(self.package.id):
            print('this package is deploying now, waiting for a while please')
            return 'This package is deploying now, , waiting for a while please'
        
        #call infrastructure deploy API
        print('deploy starting...')
        deploy_id = None
        try:
            quotas = self.get_quotas(self.deploy_instance_list)
            servers = []
            for i, ins in enumerate(self.deploy_instance_list):
                server = {}
                server['cloud'] = ins.cloud
                server['cpu'] = quotas[i]['cpu']
                server['memory'] = quotas[i]['memory']
                server['disk'] = quotas[i]['disk']
                server['server_configurations'] = ins.get_system_options()
                servers.append(server)
            deploy_infos = {"product_name":self.package.get_product_name(),
                            "servers":servers,
                            "answers":{}
                            }
            timeout_s = 10*60
            interval_s = 10
        
            deploy_id = apis.deploy(deploy_infos,  make_callback(self.package.id), timeout_s, interval_s)
        except Exception as e:
            DeployTaskManager.deploy_is_over(self.package.id)
            raise e
        
        self.package.deploy_id = deploy_id
        self.package.save()
        return 'This package is deploying now...'

    def get_quotas(self, deploy_instance_list):
        '''
        default quotas is average policy
        return:
        [{
            "cpu": 2,
            "memory": 20,
            "disk": 200,
        }],
        '''
        import math
        ins_num = len(self.deploy_instance_list)
        servers = []
        
        avg_num_cpu = math.ceil(self.plan.cpu / ins_num)
        avg_num_memory = math.ceil(self.plan.memory / ins_num)
        avg_num_disk = math.ceil(self.plan.disk / ins_num)
        for i,ins in enumerate(deploy_instance_list):
            server = {}
            
            if (i == ins_num-1):
                server['cpu'] = self.plan.cpu - avg_num_cpu * (ins_num-1)
                server['memory'] = self.plan.memory - avg_num_memory * (ins_num-1)
                server['disk'] = self.plan.disk - avg_num_disk * (ins_num-1)
            else:
                server['cpu'] = avg_num_cpu
                server['memory'] = avg_num_memory
                server['disk'] = avg_num_disk
            servers.append(server)
        return servers    

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
