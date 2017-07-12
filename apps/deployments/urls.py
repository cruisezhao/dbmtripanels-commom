from django.conf.urls import include,url
from .views4admin import (SystemOptionListView,SystemOptionView,SystemOptionEditView,SystemOptionDeleteView,
                          CloudListView, CloudView,CloudEditView,CloudDeleteView,
                          DeployPolicyListView,DeployPolicyView, DeployPolicyEditView, DeployPolicyDeleteView,
                          DeployInstanceListView,  DeployInstanceView, DeployInstanceEditView,DeployInstanceDeleteView,
                          InstanceConfigurationListView, InstanceConfigurationView, InstanceConfigurationEditView,
                          InstanceConfigurationDeleteView,QuestionListView,QuestionView,QuestionEditView,QuestionDeleteView )

urlpatterns = [
    #sys options
    url(r'^sys-options/$', SystemOptionListView.as_view(), name='sys_option_list'),
    url(r'^sys-options/(?P<uuid>[a-z\d+]{32})/$', SystemOptionView.as_view(), name='sys_option'),
    url(r'^sys-options/add/$', SystemOptionEditView.as_view(), name='sys_option_add'),
    url(r'^sys-options/(?P<uuid>[a-z\d+]{32})/edit/$', SystemOptionEditView.as_view(), name='sys_option_edit'),
    url(r'^sys-options/(?P<uuid>[a-z\d+]{32})/delete/$', SystemOptionDeleteView.as_view(), name='sys_option_delete'),

    #cloud
    url(r'^clouds/$', CloudListView.as_view(), name='cloud_list'),
    url(r'^clouds/(?P<uuid>[a-z\d+]{32})/$', CloudView.as_view(), name='cloud'),
    url(r'^clouds/add/$', CloudEditView.as_view(), name='cloud_add'),
    url(r'^clouds/(?P<uuid>[a-z\d+]{32})/edit/$', CloudEditView.as_view(), name='cloud_edit'),
    url(r'^clouds/(?P<uuid>[a-z\d+]{32})/delete/$', CloudDeleteView.as_view(), name = 'cloud_delete'),

    #deploy_policies
    url(r'^deploy-policies/$', DeployPolicyListView.as_view(), name='deploy_policy_list'),
    url(r'^deploy-policies/(?P<uuid>[a-z\d+]{32})/$', DeployPolicyView.as_view(), name='deploy_policy'),
    url(r'^deploy-policies/add/$', DeployPolicyEditView.as_view(), name='deploy_policy_add'),
    url(r'^deploy-policies/(?P<uuid>[a-z\d+]{32})/edit/$', DeployPolicyEditView.as_view(), name='deploy_policy_edit'),
    url(r'^deploy-policies/(?P<uuid>[a-z\d+]{32})/delete/$', DeployPolicyDeleteView.as_view(), name = 'deploy_policy_delete'),

    #deploy_instance
    url(r'^deploy-instances/$', DeployInstanceListView.as_view(), name='deploy_instance_list'),
    url(r'^deploy-instances/(?P<uuid>[a-z\d+]{32})/$', DeployInstanceView.as_view(), name='deploy_instance'),
    url(r'^deploy-instances/add/$', DeployInstanceEditView.as_view(), name='deploy_instance_add'),
    url(r'^deploy-instances/(?P<uuid>[a-z\d+]{32})/edit/$', DeployInstanceEditView.as_view(), name='deploy_instance_edit'),
    url(r'^deploy-instances/(?P<uuid>[a-z\d+]{32})/delete/$', DeployInstanceDeleteView.as_view(), name = 'deploy_instance_delete'),

    #instance_configuration
    url(r'^instance-configurations/$', InstanceConfigurationListView.as_view(), name='instance_configuration_list'),
    url(r'^instance-configurations/(?P<uuid>[a-z\d+]{32})/$', InstanceConfigurationView.as_view(), name='instance_configuration'),
    url(r'^instance-configurations/add/$', InstanceConfigurationEditView.as_view(), name='instance_configuration_add'),
    url(r'^instance-configurations/(?P<uuid>[a-z\d+]{32})/edit/$', InstanceConfigurationEditView.as_view(), name='instance_configuration_edit'),
    url(r'^instance-configurations/(?P<uuid>[a-z\d+]{32})/delete/$', InstanceConfigurationDeleteView.as_view(), name = 'instance_configuration_delete'),

    #questions
    url(r'^questions/$', QuestionListView.as_view(), name='question_list'),
    url(r'^questions/(?P<uuid>[a-z\d+]{32})/$', QuestionView.as_view(), name='question'),
    url(r'^questions/add/$', QuestionEditView.as_view(), name='question_add'),
    url(r'^questions/(?P<uuid>[a-z\d+]{32})/edit/$', QuestionEditView.as_view(), name='question_edit'),
    url(r'^questions/(?P<uuid>[a-z\d+]{32})/delete/$', QuestionDeleteView.as_view(), name = 'question_delete'),
]