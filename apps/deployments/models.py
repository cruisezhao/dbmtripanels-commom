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
    relationships = fields.JSONField('Relationships', default={})
    tripanels_composer_url = models.URLField('Tripanels_Composer.yml URL', max_length=256)
    
    
    class Meta:
        db_table = "deploy_policies"

class DeployInstances(CreatedUpdatedModel):    
    '''deploy instances model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)   
    policy_id = models.ForeignKey(DeployPolicies, on_delete=models.PROTECT)
    cloud_id = models.ForeignKey(Clouds, on_delete=models.PROTECT)
    relationships = fields.JSONField('Relationships', default={})
    
    class Meta:
        db_table = 'deploy_instances'

class InstanceConfigurations(CreatedUpdatedModel):        
    '''instance configurations model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)    
    deploy_instance_id = models.ForeignKey(DeployInstances, on_delete=models.PROTECT)
    option_id = models.ForeignKey(SystemOptions, on_delete=models.PROTECT)
     
    class Meta:
        db_table = 'instance_configurations'   
      
class Questions(CreatedUpdatedModel):  
    '''questions for product deploy'''
    
    TYPE_CHOICE = [
        ('string', 'string'),
        ('enum', 'enum'),
        ('integer', 'integer'),
    ]
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    product_id = models.ForeignKey(Products, on_delete=models.PROTECT)
    name = models.CharField('Name', max_length=32)
    label = models.CharField('Label', max_length=64)
    description = models.CharField('Description', max_length=100, null = True, blank = True)
    type = models.CharField('Type', max_length=32, default=TYPE_CHOICE[0], choices=TYPE_CHOICE)
    default = models.CharField('Default Value', max_length=64, null = True, blank = True)
    required = models.BooleanField('Required', default=True)
    hidden = models.BooleanField('Hidden', default=True)
    options = fields.JSONField('Options', default={})
    
    class Meta:
        db_table = 'questions'   
    