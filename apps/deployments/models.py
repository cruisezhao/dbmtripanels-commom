from django.db import models
from common.utilities.models import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from jsonfield import fields
from common.apps.products.models import Products

# Create your models here.

class SystemOptions(CreatedUpdatedModel):
    '''system options model'''
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    type = models.CharField('Type', max_length=32)
    name = models.CharField('Name', unique=True, max_length=32)
    value = models.CharField('Value', max_length=64)
    label = models.CharField('Label', max_length=64)
    
    class Meta:
        db_table = "system_options"

    def __str__(self):
        return self.name
    
class Clouds(CreatedUpdatedModel):
    '''clouds model'''
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    name = models.CharField('Name', max_length=100)
    
    class Meta:
        db_table = "clouds"

    def __str__(self):
        return self.name
        
class DeployPolicies(CreatedUpdatedModel):
    """Deploy Policies model"""
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    product =  models.ForeignKey(Products, on_delete=models.PROTECT)
    relationships = fields.JSONField('Relationships', default={})
    tripanels_composer_url = models.URLField('Tripanels_Composer.yml URL', max_length=256)
    
    
    class Meta:
        db_table = "deploy_policies"

    def __str__(self):
        return "{}-{}".format(self.product.product_name,self.tripanels_composer_url)

class DeployInstances(CreatedUpdatedModel):    
    '''deploy instances model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)   
    deploy_policy = models.ForeignKey(DeployPolicies, on_delete=models.PROTECT)
    cloud = models.ForeignKey(Clouds, on_delete=models.PROTECT)
    relationships = fields.JSONField('Relationships', default={})
    
    class Meta:
        db_table = 'deploy_instances'
        
    def get_options_by_type(self):
        groups = {}
        for config in self.instanceconfigurations_set:
            if config.system_option.type not in groups:
                groups[config.system_option.type] = []
            groups[config.system_option.type].append(config.system_option)
        return groups        
            

class InstanceConfigurations(CreatedUpdatedModel):        
    '''instance configurations model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)    
    deploy_instance = models.ForeignKey(DeployInstances, on_delete=models.PROTECT)
    system_option = models.ForeignKey(SystemOptions, on_delete=models.PROTECT)
     
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
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    name = models.CharField('Name', max_length=32)
    label = models.CharField('Label', max_length=64)
    description = models.CharField('Description', max_length=100, null = True, blank = True)
    type = models.CharField('Type', max_length=32, default=TYPE_CHOICE[0], choices=TYPE_CHOICE)
    default = models.CharField('Default Value', default='', max_length=64, null = True, blank = True)
    required = models.BooleanField('Required', default=True)
    hidden = models.BooleanField('Hidden', default=True)
    options = fields.JSONField('Options', default={})
    
    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.name
    