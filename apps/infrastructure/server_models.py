from django.db import models
from common.utilities.utils import uuid_to_str
from .network_models import Datacenters, CloudConsoles, RackUnits, Vendors, NetworkPorts, PowerOutlets
from common.apps.clients.models import Clients
from common.apps.deployments.models import SystemOptions
from common.apps.users.models import Users

SERVER_STATUS = (
    ('Deploying', 'Deploying'),
    ('DeployFailed','DeployFailed'),
    ('Running','Running'),
    ('Deleted','Deleted'),
)

SERVER_TYPE = (
    ('BareMetal', 'BareMetal'),
    ('VirtualMachine', 'VirtualMachine'),
    ('Container', 'Container'),
)

NETWORKPORT_STATUS = (
    ('On','On'),
    ('Off','Off'),
)

PARTITION_STATUS = (
    ('Online','Online'),
    ('Offline','Offline'),
)

MAINTENACE_STATUS = (
    ('Maintaining','Maintaining'),
    ('Finished','Finished'),
)

POWEROUTLET_STATUS = (
    ('On','On'),
    ('Off','Off'),
)

POWEROUTLET_TYPE = (
    ('TwoHoles','TwoHoles'),
    ('ThreeHoles', 'ThreeHoles'),
)

class Servers(models.Model):
    """Servers"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    datacenter = models.ForeignKey(Datacenters, models.SET_NULL, null=True, blank=True)
    cloud = models.ForeignKey(CloudConsoles, models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Clients, models.SET_NULL, null=True, blank=True)
    host_id = models.CharField(max_length=255, null=True, blank=True)
    peer_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=32, null=True, blank=True)
    tag = models.CharField(max_length=32, null=True, blank=True)
    type = models.CharField(max_length=32, choices=SERVER_TYPE, null=True, blank=True)
    virtualization_type = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=32, choices=SERVER_STATUS)
    cpu_speed = models.DecimalField('Total Fee', max_digits=10, decimal_places=2, null=True, blank=True)
    total_cores = models.PositiveSmallIntegerField('CPU Cores', null=True, blank=True)
    total_memory = models.CharField(max_length=32, null=True, blank=True)
    notes = models.CharField(max_length=1024, null=True, blank=True)
    build_date = models.DateTimeField('Build Date', null=True, blank=True)
    online_date = models.DateTimeField('Online Date', null=True, blank=True)
    offline_date = models.DateTimeField('Offline Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    rent_start_date = models.DateTimeField('Rent Start Date', null=True, blank=True)
    rent_end_date = models.DateTimeField('Rent End Date', null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    created_by = models.PositiveIntegerField('Created By', null=True, blank=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)
    updated_by = models.PositiveIntegerField('Updated Date', null=True, blank=True)

    class Meta:
        db_table = "servers"
        ordering = ['-created_date']

class ServerContainers(models.Model):
    """Containers"""
    server = models.OneToOneField(Servers, primary_key=True)
    stack_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "server_containers"
        ordering = ['-created_date']

class ServerVMs(models.Model):
    """Virtual Machines"""
    server = models.OneToOneField(Servers, primary_key=True)

    class Meta:
        db_table = "server_vms"
        ordering = ['-created_date']

class ServerBareMetals(models.Model):
    """Bare Metals"""
    server = models.OneToOneField(Servers, primary_key=True)
    rack_unit = models.ForeignKey(RackUnits, models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendors, models.SET_NULL, null=True, blank=True)
    processor_model = models.CharField(max_length=32, null=True, blank=True)
    no_of_processors = models.PositiveSmallIntegerField('CPU Cores', null=True, blank=True)
    memory_chips = models.CharField(max_length=32, null=True, blank=True)
    motherboard_model = models.CharField(max_length=32, null=True, blank=True)
    chassis_model = models.CharField(max_length=32, null=True, blank=True)
    power_supply_model = models.CharField(max_length=32, null=True, blank=True)
    with_rail = models.NullBooleanField()

    class Meta:
        db_table = "server_baremetals"
        ordering = ['-created_date']

class ServerConfigurations(models.Model):
    """deploy  Configurations"""
    server = models.ForeignKey(Servers)
    system_option = models.ForeignKey(SystemOptions)

    class Meta:
        db_table = "server_configurations"
        ordering = ['-created_date']

class ServerNetworkports(models.Model):
    """Server Networkports"""
    server = models.ForeignKey(Servers)
    networkport = models.ForeignKey(NetworkPorts)
    port_number = models.PositiveSmallIntegerField('Port Number', null=True, blank=True)
    port_speed = models.PositiveIntegerField('Updated Date', null=True, blank=True)
    interface_name = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=32, null=True, blank=True)
    install_date = models.DateTimeField('Install Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    status = models.CharField(max_length=32, choices=NETWORKPORT_STATUS)
    notes = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "server_networkports"
        ordering = ['-created_date']

class ServerPartitions(models.Model):
    """Server Partitions"""
    server = models.ForeignKey(Servers)
    disk_type = models.CharField(max_length=32, null=True, blank=True)
    raid_type = models.CharField(max_length=32, null=True, blank=True)
    file_system = models.CharField(max_length=32, null=True, blank=True)
    path = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=32, choices=PARTITION_STATUS)
    totalGB = created_by = models.PositiveIntegerField('Total GB', null=True, blank=True)
    disk_info = models.CharField(max_length=1024, null=True, blank=True)
    install_date = models.DateTimeField('Install Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    notes = models.CharField(max_length=1024, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    created_by = models.PositiveIntegerField('Created By', null=True, blank=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)
    updated_by = models.PositiveIntegerField('Updated Date', null=True, blank=True)

    class Meta:
        db_table = "server_partitions"
        ordering = ['-created_date']

class ServerMaintenaces(models.Model):
    """Server Maintenaces"""
    server = models.ForeignKey(Servers)
    user = models.ForeignKey(Users)
    start_time = models.DateTimeField('Start Time', null=True, blank=True)
    end_time = models.DateTimeField('End Time', null=True, blank=True)
    task_subject = models.CharField(max_length=64, null=True, blank=True)
    task_detail = models.CharField(max_length=1024, null=True, blank=True)
    total_minutes = models.PositiveIntegerField('Total Minutes', null=True, blank=True)
    status = models.CharField(max_length=32, choices=MAINTENACE_STATUS)
    notes = models.CharField(max_length=1024, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    created_by = models.PositiveIntegerField('Created By', null=True, blank=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)
    updated_by = models.PositiveIntegerField('Updated Date', null=True, blank=True)

    class Meta:
        db_table = "server_maintenaces"
        ordering = ['-created_date']

class ServerPoweroutlets(models.Model):
    """Server Poweroutlets"""
    server = models.ForeignKey(Servers)
    power_outlet = models.ForeignKey(PowerOutlets)
    port_number = models.PositiveIntegerField('Port Number', null=True, blank=True)
    type = models.CharField(max_length=32, choices=POWEROUTLET_TYPE)
    install_date = models.DateTimeField('Install Date', null=True, blank=True)
    terminate_date = models.DateTimeField('Terminate Date', null=True, blank=True)
    status = models.CharField(max_length=32, choices=POWEROUTLET_STATUS)
    notes = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "server_poweroutlets"
        ordering = ['-created_date']

