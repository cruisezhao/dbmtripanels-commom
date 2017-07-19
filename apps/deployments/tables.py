import django_tables2 as tables
from django_tables2.utils import A
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)
from common.utilities.tables import ToggleColumn

SysOption_ACTIONS = """
    <a href="{% url 'deployments:sys_option_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>
"""

class SysOptionTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:sys_option', args=[A('uuid')])
    name = tables.LinkColumn('deployments:sys_option', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=SysOption_ACTIONS, orderable=False)
    class Meta:
        model = SystemOptions
        fields = ['pk','id', 'name', 'type','value','action']

Cloud_ACTIONS = """<a href="{% url 'deployments:cloud_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>"""
class CloudTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:cloud', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=Cloud_ACTIONS, orderable=False)
    class Meta:
        model = Clouds
        fields = ['pk','id', 'name', 'action']

Deploy_Policy_ACTIONS = """<a href="{% url 'deployments:deploy_policy_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>"""
class DeployPolicyTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:deploy_policy', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=Deploy_Policy_ACTIONS, orderable=False)
    class Meta:
        model = DeployPolicies
        fields = ['pk','id', 'relationships','action']

Deploy_Instance_ACTIONS = """<a href="{% url 'deployments:deploy_instance_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>"""
class DeployInstanceTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:deploy_instance', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=Deploy_Instance_ACTIONS, orderable=False)
    class Meta:
        model = DeployInstances
        fields = ['pk','id','deploy_policy','action']

Instance_Configuration_ACTIONS = """<a href="{% url 'deployments:instance_configuration_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>"""
class InstanceConfigurationTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:instance_configuration', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=Instance_Configuration_ACTIONS, orderable=False)
    class Meta:
        model = InstanceConfigurations
        fields = ['pk','id','deploy_instance','action']

Question_ACTIONS = """<a href="{% url 'deployments:question_edit' uuid=record.uuid %}"><i class='fa fa-pencil'></i></a>"""
class QuestionTable(tables.Table):
    pk = ToggleColumn()
    id = tables.LinkColumn('deployments:question', args=[A('uuid')])
    action = tables.TemplateColumn(template_code=Question_ACTIONS, orderable=False)
    class Meta:
        model = Questions
        fields = ['pk','id','name','type','required','action']