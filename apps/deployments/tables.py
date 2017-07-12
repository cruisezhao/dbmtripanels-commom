import django_tables2 as tables
from django_tables2.utils import A
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)

class SysOptionTable(tables.Table):
    id = tables.LinkColumn('deployments:sys_option', args=[A('uuid')])

    class Meta:
        model = SystemOptions
        fields = ['id', 'name', 'value']


class CloudTable(tables.Table):
    id = tables.LinkColumn('deployments:cloud', args=[A('uuid')])

    class Meta:
        model = Clouds
        fields = ['id', 'name']


class DeployPolicyTable(tables.Table):
    id = tables.LinkColumn('deployments:deploy_policy', args=[A('uuid')])

    class Meta:
        model = DeployPolicies
        fields = ['id', 'relationships']


class DeployInstanceTable(tables.Table):
    id = tables.LinkColumn('deployments:deploy_instance', args=[A('uuid')])

    class Meta:
        model = DeployInstances
        fields = ['id','deploy_policy']


class InstanceConfigurationTable(tables.Table):
    id = tables.LinkColumn('deployments:instance_configuration', args=[A('uuid')])

    class Meta:
        model = InstanceConfigurations
        fields = ['id','deploy_instance']


class QuestionTable(tables.Table):
    id = tables.LinkColumn('deployments:question', args=[A('uuid')])

    class Meta:
        model = Questions
        fields = ['id','name','type','required']