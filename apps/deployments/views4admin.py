from django.views.generic import View
from django.shortcuts import get_object_or_404,render
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)
from . import tables
from . import forms
from . import filters
from common.utilities.views import (ObjectListView,ObjectEditView,
                                    ObjectDeleteView)
from utilities.views import BaseDetailView

class SystemOptionListView(ObjectListView):
    queryset = SystemOptions.objects.all()
    filter = filters.SysOptionFilter
    filter_form = forms.SysOptionFilterForm
    table = tables.SysOptionTable
    template_name = "deployments/sys_option_list.html"


class SystemOptionView(View):
    def get(self, request, uuid):
        sys_option = get_object_or_404(SystemOptions,uuid = uuid)
        return render(request, "deployments/sys_option.html",
                      {'object':sys_option})


class SystemOptionEditView(ObjectEditView):
    """product edit"""
    model = SystemOptions
    form_class = forms.SystemOptionForm
    template_name = 'deployments/sys_option_edit.html'
    default_return_url = 'deployments:sys_option_list'


class SystemOptionDeleteView(ObjectDeleteView):
    model = SystemOptions
    default_return_url = "deployments:sys_option_list"


class CloudListView(ObjectListView):
    queryset = Clouds.objects.all()
    filter = filters.CloudFilter
    filter_form = None
    table = tables.CloudTable
    template_name = 'deployments/cloud_list.html'


class CloudView(View):
    def get(self,request, uuid):
        cloud = get_object_or_404(Clouds, uuid = uuid)
        return render(request, 'deployments/cloud.html',{
            'object':cloud,
        })


class CloudEditView(ObjectEditView):
    model = Clouds
    form_class = forms.CloudForm
    template_name = 'deployments/cloud_edit.html'
    default_return_url = 'deployments:cloud_list'


class CloudDeleteView(ObjectDeleteView):
    model = Clouds
    default_return_url = 'deployments:cloud_list'


class DeployPolicyListView(ObjectListView):
    queryset = DeployPolicies.objects.all()
    filter = filters.DeployPolicyFilter
    filter_form = None
    table = tables.DeployPolicyTable
    template_name = "deployments/deploy_policy_list.html"


# class DeployPolicyView(View):
#     def get(self,request, uuid):
#         deploy = get_object_or_404(DeployPolicies, uuid = uuid)
#         return render(request, 'deployments/deploy_policy.html',{
#             'object':deploy,
#         })

class DeployPolicyView(BaseDetailView):
    model = DeployPolicies
    template_name = 'deployments/deploy_policy.html'
    class Groups:
        from collections import OrderedDict
        groups = OrderedDict([('Group1', ('uuid',)), ('Group2', ('plan', 'product'))])

class DeployPolicyEditView(ObjectEditView):
    model = DeployPolicies
    form_class = forms.DeployPolicyForm
    template_name = "deployments/deploy_policy_edit.html"
    default_return_url = "deployments:deploy_policy_list"

class DeployPolicyDeleteView(ObjectDeleteView):
    model = DeployPolicies
    default_return_url = "deployments:deploy_policy_list"

class DeployInstanceListView(ObjectListView):
    queryset=  DeployInstances.objects.all()
    filter = filters.DeployInstanceFilter
    filter_form = None
    table = tables.DeployInstanceTable
    template_name = "deployments/deploy_instance_list.html"


class DeployInstanceView(View):
    def get(self,request, uuid):
        deploy_instance = get_object_or_404(DeployInstances, uuid = uuid)
        return render(request, 'deployments/deploy_instance.html',{
            'object':deploy_instance,
        })



class DeployInstanceEditView(ObjectEditView):
    model = DeployInstances
    form_class = forms.DeployInstanceForm
    template_name = "deployments/deploy_instance_edit.html"
    default_return_url = "deployments:deploy_instance_list"


class DeployInstanceDeleteView(ObjectDeleteView):
    model = DeployInstances
    default_return_url = "deployments:deploy_instance_list"


class InstanceConfigurationListView(ObjectListView):
    queryset = InstanceConfigurations.objects.all()
    filter = filters.InstanceConfigurationFilter
    filter_form = None
    table = tables.InstanceConfigurationTable
    template_name = "deployments/instance_configuration_list.html"

class InstanceConfigurationView(View):
    def get(self,request, uuid):
        instance_configuration = get_object_or_404(InstanceConfigurations, uuid = uuid)
        return render(request, 'deployments/instance_configuration.html',{
            'object':instance_configuration,
        })


class InstanceConfigurationEditView(ObjectEditView):
    model = InstanceConfigurations
    form_class = forms.InstanceConfigurationForm
    template_name = "deployments/instance_configuration_edit.html"
    default_return_url = "deployments:instance_configuration_list"


class InstanceConfigurationDeleteView(ObjectDeleteView):
    model = InstanceConfigurations
    default_return_url = "deployments:instance_configuration_list"


class QuestionListView(ObjectListView):
    queryset = Questions.objects.all()
    filter = filters.QuestionFilter
    filter_form = None
    table = tables.QuestionTable
    template_name = "deployments/question_list.html"


class QuestionView(View):
    def get(self,request, uuid):
        question = get_object_or_404(Questions, uuid = uuid)
        return render(request, 'deployments/question.html',{
            'object':question,
        })


class QuestionEditView(ObjectEditView):
    model = Questions
    form_class = forms.QuestionForm
    template_name = 'deployments/question_edit.html'
    default_return_url = "deployments:question_list"


class QuestionDeleteView(ObjectDeleteView):
    model = Questions
    default_return_url = "deployments:question_list"