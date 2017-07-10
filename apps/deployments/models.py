from django.db import models
from common.utilities.models import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from jsonfield import fields
from common.apps.products.models import Products

# Create your models here.

class SystemOptions(CreatedUpdatedModel):
    '''system options model'''
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    name = models.CharField('Name', max_length=32)
    value = models.CharField('Value', max_length=64)
    
    class Meta:
        db_table = "system_options"
    
class Clouds(CreatedUpdatedModel):
    '''clouds model'''
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    name = models.CharField('Name', max_length=100)
    
    class Meta:
        db_table = "clouds"
        
class DeployPolicies(CreatedUpdatedModel):
    """Deploy Policies model"""
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    product_id =  models.ForeignKey(Products, on_delete=models.PROTECT)
    relationships = fields.JSONField('relationships', default={})
    
    class Meta:
        db_table = "deploy_policies"

class DeployInstances(CreatedUpdatedModel):    
    '''deploy instances model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)   
    policy_id = models.ForeignKey(DeployPolicies, on_delete=models.PROTECT)
    cloud_id = models.ForeignKey(Clouds, on_delete=models.PROTECT)
    relationships = fields.JSONField('relationships', default={})
    cpu = models.IntegerField('CPU',default=0)
    memory = models.IntegerField('Memory', default=0)
    disk = models.IntegerField('Disk', default = 0)
    
    class Meta:
        db_table = 'deploy_instances'

class InstanceConfigurations(CreatedUpdatedModel):        
    '''instance configurations model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)    
    deploy_instance_id = models.ForeignKey(DeployInstances, on_delete=models.PROTECT)
    option_id = models.ForeignKey(SystemOptions, on_delete=models.PROTECT)
     
    class Meta:
        db_table = 'instance_configurations'   
        