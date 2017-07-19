from django.db import models
from common.utilities.models import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from jsonfield import fields
from common.apps.products.models import Products, Plans
from common.apps.users.models import Users
from common.apps.packages.models import Packages

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
    plan =  models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True, blank=True)
    product =  models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    relationships = fields.JSONField('Relationships', default={})
    #tripanels_composer_url = models.URLField('Tripanels_Composer.yml URL', max_length=256)
    
    
    class Meta:
        db_table = "deploy_policies"

    def __str__(self):
         return "policies-{}".format(self.uuid[:4])

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
        for config in self.instanceconfigurations_set.all():
            if config.system_option.type not in groups:
                groups[config.system_option.type] = []
            groups[config.system_option.type].append(config.system_option)
        return groups

    def __str__(self):
        return "{}-{}".format('instance',self.cloud.name)
    
    def get_system_options(self):
        options = []
        for config in self.instanceconfigurations_set.all():
            options.append(config.system_option)
        return options
    
class InstanceConfigurations(CreatedUpdatedModel):        
    '''instance configurations model''' 
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)    
    deploy_instance = models.ForeignKey(DeployInstances, on_delete=models.PROTECT)
    system_option = models.ForeignKey(SystemOptions, on_delete=models.PROTECT)
     
    class Meta:
        db_table = 'instance_configurations'

    def __str__(self):
        return '{}-{}'.format(self.deploy_instance,self.system_option.name)
      
class Questions(CreatedUpdatedModel):  
    '''questions for product deploy'''
    
    TYPE_CHOICE = [
        ('string', 'string'),
        ('password', 'password'),
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
    hidden = models.BooleanField('Hidden', default=False)
    options = fields.JSONField('Options', default={})
    
    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.name
    

class Devices(models.Model):
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)

class Servers(CreatedUpdatedModel):
    """Servers"""
    SERVER_TYPE = (
        ('BareMetal', 'BareMetal'),
        ('VirtualMachine', 'VirtualMachine'),
        ('Container', 'Container'),
    )
    
    SERVER_STATUS = (
        ('Deploying', 'Deploying'),
        ('DeployFailed','DeployFailed'),
        ('Running','Running'),
        ('Deleted','Deleted'),
    )

    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    cloud = models.ForeignKey(Clouds, models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(Packages,on_delete=models.PROTECT, null=True, blank=True)
    device = models.ForeignKey(Devices, on_delete=models.PROTECT, null=True, blank=True)
    peer_id = models.CharField(max_length=255, null=True, blank=True)
    deploy_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=32, null=True, blank=True)
    tag = models.CharField(max_length=32, null=True, blank=True)
    type = models.CharField(max_length=32, choices=SERVER_TYPE, null=True, blank=True)
    virtualization_type = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=32, choices=SERVER_STATUS)
    cpu_speed = models.DecimalField('Total Fee', max_digits=10, decimal_places=2, null=True, blank=True)
    total_cores = models.PositiveSmallIntegerField('CPU Cores', null=True, blank=True)
    total_memory = models.PositiveIntegerField('Memory(M)', null=True, blank=True)
    notes = models.CharField(max_length=1024, null=True, blank=True)
    build_date = models.DateTimeField('Build Date', null=True, blank=True)
    online_date = models.DateTimeField('Online Date', null=True, blank=True)
    offline_date = models.DateTimeField('Offline Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    rent_start_date = models.DateTimeField('Rent Start Date', null=True, blank=True)
    rent_end_date = models.DateTimeField('Rent End Date', null=True, blank=True)
    system_options = models.ManyToManyField(SystemOptions, db_table='server_configurations')
    
    class Meta:
        db_table = "servers"
        
        
    def is_container(self):
        return self.type == 'Container'
    
    def is_VM(self):
        return self.type == 'VirtualMachine'
    
    @classmethod
    def is_type_container(cls, t):
        return t == 'Container'

    @classmethod
    def is_type_VM(cls, t):
        return t == 'VirtualMachine'
    
class ServerContainers(Servers):
    """Containers"""
    #server = models.OneToOneField(Servers, primary_key=True)
    stack_id = models.CharField(max_length=255, null=True, blank=True)
    service_id = models.CharField(max_length=255, null=True, blank=True)
    container_id = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        db_table = "server_containers"

class ServerVMs(Servers):
    """Virtual Machines"""
    #server = models.OneToOneField(Servers, primary_key=True)

    class Meta:
        db_table = "server_vms"


class ServerBareMetals(Servers):
    """Bare Metals"""
    #server = models.OneToOneField(Servers, primary_key=True)

    class Meta:
        db_table = "server_baremetals"

# class ServerConfigurations(CreatedUpdatedModel):
#     """deploy  Configurations"""
#     server = models.ForeignKey(Servers)
#     system_option = models.ForeignKey(SystemOptions)
# 
#     class Meta:
#         db_table = "server_configurations"


class ServerPartitions(CreatedUpdatedModel):
    """Server Partitions"""
    PARTITION_STATUS = (
        ('Online','Online'),
        ('Offline','Offline'),
    )
    server = models.ForeignKey(Servers)
    disk_type = models.CharField(max_length=32, null=True, blank=True)
    raid_type = models.CharField(max_length=32, null=True, blank=True)
    file_system = models.CharField(max_length=32, null=True, blank=True)
    path = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=32, choices=PARTITION_STATUS)
    totalGB = models.PositiveIntegerField('Total GB', null=True, blank=True)
    disk_info = models.CharField(max_length=1024, null=True, blank=True)
    install_date = models.DateTimeField('Install Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    notes = models.CharField(max_length=1024, null=True, blank=True)


    class Meta:
        db_table = "server_partitions"


class ServerMaintenances(CreatedUpdatedModel):
    """Server Maintenances"""
    MAINTENACE_STATUS = (
        ('Maintaining','Maintaining'),
        ('Finished','Finished'),
    )
    server = models.ForeignKey(Servers)
    user = models.ForeignKey(Users)
    start_time = models.DateTimeField('Start Time', null=True, blank=True)
    end_time = models.DateTimeField('End Time', null=True, blank=True)
    task_subject = models.CharField('Task Subject',max_length=64, null=True, blank=True)
    task_detail = models.CharField('Task Details',max_length=1024, null=True, blank=True)
    total_minutes = models.PositiveIntegerField('Total Minutes', null=True, blank=True)
    status = models.CharField('Status', max_length=32, choices=MAINTENACE_STATUS)
    notes = models.CharField('Notes', max_length=1024, null=True, blank=True)


    class Meta:
        db_table = "server_maintenances"
        
