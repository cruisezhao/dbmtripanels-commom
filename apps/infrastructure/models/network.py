from django.db import models
from .util import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from common.apps.users.models import Users
from phonenumber_field.modelfields import PhoneNumberField
from django.core.urlresolvers import reverse


class Vendors(CreatedUpdatedModel):
    """Vendors"""
    VENDOR_TYPE = (
        ('Manufacturer', 'Manufacturer'),
        ('Seller', 'Seller'),
        ('ProductVendor', 'ProductVendor'),
        ('CloudProvider', 'CloudProvider'),
    )

    VENDOR_STATUS = (
        ('Active', 'Active'),
        ('Deprecated', 'Deprecated'),
    )

    type = models.CharField(max_length=32, choices=VENDOR_TYPE)
    name = models.CharField(max_length=256,null=True,blank=True)
    description = models.TextField(blank=True)
    website = models.CharField(max_length=256,null=True,blank=True)
    address = models.CharField(max_length=256,null=True,blank=True)
    city = models.CharField(max_length=32,null=True,blank=True)
    state = models.CharField(max_length=32,null=True,blank=True)
    country = models.CharField(max_length=32,null=True,blank=True)
    zip = models.CharField(max_length=32,null=True,blank=True)
    phone = PhoneNumberField('Phone Number',null=True,blank=True)
    support_email = models.CharField(max_length=128,null=True,blank=True)
    support_portal = models.CharField(max_length=128,null=True,blank=True)
    username = models.CharField(max_length=128,null=True,blank=True)
    password = models.CharField(max_length=128,null=True,blank=True)
    status = models.CharField(max_length=32, choices=VENDOR_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "vendors"

    def __str__(self):
        return self.name


class DataCenters(CreatedUpdatedModel):
    """Data Centers"""
    DATA_CENTER_STATUS = (
        ('Active', 'Active'),
        ('Deprecated', 'Deprecated'),
    )

    name = models.CharField(max_length=256,null=True,blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=256,null=True,blank=True)
    region = models.CharField(max_length=32,null=True,blank=True)
    city = models.CharField(max_length=32,null=True,blank=True)
    state = models.CharField(max_length=32,null=True,blank=True)
    country = models.CharField(max_length=32,null=True,blank=True)
    zip = models.CharField(max_length=64,null=True,blank=True)
    website = models.CharField(max_length=128,null=True,blank=True)
    phone = PhoneNumberField('Phone Number',null=True,blank=True)
    support_email = models.CharField(max_length=128,null=True,blank=True)
    support_portal = models.CharField(max_length=128,null=True,blank=True)
    username = models.CharField(max_length=128,null=True,blank=True)
    password = models.CharField(max_length=128,null=True,blank=True)
    status = models.CharField(max_length=32, choices=DATA_CENTER_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "data_centers"

    def __str__(self):
        return self.name


class Devices(CreatedUpdatedModel):
    """Devices"""
    DEVICE_TYPE = (
        ('Rack', 'Rack'),
        ('Power', 'Power'),
        ('Drive', 'Drive'),
        ('KVM', 'KVM'),
        ('Router', 'Router'),
        ('Switch', 'Switch'),
        ('Firewall', 'Firewall'),
        ('BareMetal', 'BareMetal'),
    )

    DEVICE_STATUS = (
        ('PowerOn', 'PowerOn'),
        ('PowerOff', 'PowerOff'),
        ('InMaintenance', 'InMaintenance'),
        ('Deprecated', 'Deprecated'),
    )

    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(Vendors, models.SET_NULL, related_name='manufacturer_device', null=True, blank=True)
    seller = models.ForeignKey(Vendors, models.SET_NULL, related_name='seller_device', null=True, blank=True)
    name = models.CharField(max_length=256,null=True,blank=True)
    tag = models.CharField(max_length=128,null=True,blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=32, choices=DEVICE_TYPE)
    u_height = models.PositiveSmallIntegerField(verbose_name='Height In Rack', null=True, blank=True,
                                                help_text='How many rack units does this device occupy')
    size = models.CharField(max_length=128,null=True,blank=True)
    model_no = models.CharField(max_length=128,null=True,blank=True)
    serial_no = models.CharField(max_length=128, blank=True, verbose_name='Serial Number')
    # rack = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Rack')
    # rack_start_unit =  models.ForeignKey(Interfaces, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Rack Unit')
    online_date = models.DateField('Online Date', null=True, blank=True)
    offline_date = models.DateField('Offline Date', null=True, blank=True)
    order_date = models.DateField('Order Date', null=True, blank=True)
    price = models.DecimalField('Price',max_digits=10, decimal_places=2)
    order_no = models.CharField(max_length=256,null=True,blank=True)
    warranty_date = models.DateField('Warranty Date', null=True, blank=True)
    access_method = models.CharField(max_length=32,null=True,blank=True)
    access_url = models.CharField(max_length=256,null=True,blank=True)
    access_port = models.PositiveIntegerField(null=True, blank=True)
    username = models.CharField(max_length=128,null=True,blank=True)
    password = models.CharField(max_length=128,null=True,blank=True)
    status = models.CharField(max_length=32, choices=DEVICE_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "devices"

    def __str__(self):
        return self.name

class DeviceRacks(Devices):
    """Racks"""
    location = models.CharField(max_length=256, help_text='How to find the rack in data center.')
    network_tag = models.CharField(max_length=64,null=True,blank=True)
    network_speed = models.PositiveIntegerField(null=True, blank=True)
    max_bandwidth = models.PositiveIntegerField(null=True, blank=True)
    used_bandwidth = models.PositiveIntegerField(null=True, blank=True)
    bw_check_date = models.DateField('Band Width Check Date', null=True, blank=True, help_text='Band Width Check Date')
    routing_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True)
    routing_gateway = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True)
    routing_mask = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True)

    class Meta:
        db_table = "device_racks"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('infras:rack_list')

    def get_detail_url(self):
        return reverse('infras:rack', args=(self.uuid,))


class DevicePowers(Devices):
    """Power Devices"""
    POWER_COLOR = (
        ('Black','Black'),
        ('Red','Red')
    )

    total_outlets = models.PositiveSmallIntegerField(verbose_name='Power Outlet Amount', null=True, blank=True)
    max_amps = models.PositiveIntegerField(null=True, blank=True)
    used_amps = models.PositiveIntegerField(null=True, blank=True)
    check_date = models.DateField('Check Date', null=True, blank=True, help_text='Check Date')
    voltage = models.PositiveSmallIntegerField(verbose_name='Voltage', null=True, blank=True)
    color = models.CharField(max_length=32, choices=POWER_COLOR, null=True, blank=True)

    class Meta:
        db_table = "device_powers"

    def __str__(self):
        return self.name

class DeviceDrives(Devices):
    """Drives"""
    DISK_TYPE = (
        ('SATA', 'SATA'),
        ('SSD', 'SSD'),
    )

    disk_type = models.CharField(max_length=32, choices=DISK_TYPE, null=True, blank=True)
    disk_size = models.PositiveIntegerField(null=True, blank=True)
    file_system = models.CharField(max_length=64,null=True,blank=True)
    need_power = models.NullBooleanField()

    class Meta:
        db_table = "device_drives"

    def __str__(self):
        return self.name

class DeviceKVMs(Devices):
    """KVMs"""
    KVM_PORT_TYPE = (
        ('USB', 'USB'),
        ('PS2', 'PS2'),
    )

    total_ports = models.PositiveSmallIntegerField(null=True, blank=True)
    port_type = models.CharField(max_length=32, choices=KVM_PORT_TYPE, null=True, blank=True)

    class Meta:
        db_table = "device_kvms"

    def __str__(self):
        return self.name

class DeviceRouters(Devices):
    """Routers"""
    firmware_version = models.CharField(max_length=128, null=True, blank=True)
    total_ports = models.PositiveSmallIntegerField(null=True, blank=True)
    speed = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_routers"

    def __str__(self):
        return self.name

class DeviceSwitches(Devices):
    """Switches"""

    firmware_version = models.CharField(max_length=128, null=True, blank=True)
    total_ports = models.PositiveSmallIntegerField(null=True, blank=True)
    speed = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_switches"

    def __str__(self):
        return self.name

class DeviceFirewalls(Devices):
    """Firewalls"""
    firmware_version = models.CharField(max_length=128,null=True,blank=True)
    total_ports = models.PositiveSmallIntegerField(null=True, blank=True)
    total_licenses = models.PositiveSmallIntegerField(null=True, blank=True)
    speed = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_firewalls"

    def __str__(self):
        return self.name

class DeviceBares(Devices):
    """Bare Metals"""
    RAID_TYPE = (
        ('USB', 'USB'),
        ('PS2', 'PS2'),
    )

    BARE_FIRMWARE_TYPE = (
        ('BIOS', 'BIOS'),
        ('UEFI', 'UEFI'),
    )

    cpu_model = models.CharField(max_length=128, null=True, blank=True)
    total_cpus = models.PositiveSmallIntegerField('CPUs', null=True, blank=True)
    total_cores = models.PositiveSmallIntegerField('Cores', null=True, blank=True)
    cpu_speed = models.CharField(max_length=64, null=True, blank=True)
    memory_model = models.CharField(max_length=128, null=True, blank=True)
    memory_size = models.DecimalField('Price',max_digits=10, decimal_places=2)
    motherboard_model = models.CharField(max_length=128,null=True,blank=True)
    chassis_model = models.CharField(max_length=128,null=True,blank=True)
    power_supply_model = models.CharField(max_length=128,null=True,blank=True)
    disk_size = models.PositiveIntegerField(null=True, blank=True)
    disk_description = models.TextField(blank=True)
    has_raid = models.NullBooleanField()
    raid_type = models.CharField(max_length=64,null=True,blank=True)
    has_ipmi = models.NullBooleanField()
    ipmi_username = models.CharField(max_length=128,null=True,blank=True)
    ipmi_password = models.CharField(max_length=128,null=True,blank=True)
    ipmi_version = models.CharField(max_length=32,null=True,blank=True)
    total_ports = models.PositiveSmallIntegerField(null=True, blank=True)
    firmware_type = models.CharField(max_length=32, choices=BARE_FIRMWARE_TYPE, null=True, blank=True)
    firmware_version = models.CharField(max_length=32,null=True,blank=True)
    usage = models.CharField(max_length=64,null=True,blank=True)

    class Meta:
        db_table = "device_bares"

    def __str__(self):
        return self.name

class DeviceMaintenances(CreatedUpdatedModel):
    """Device Maintenances"""
    MAINTENANCE_STATUS = (
        ('InProcess','InProcess'),
        ('HangUp', 'HangUp'),
        ('Finished', 'Finished'),
    )

    device = models.ForeignKey(Devices, models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Users, models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField('Start Time', null=True, blank=True)
    end_time = models.DateTimeField('End Time', null=True, blank=True)
    subject = models.CharField(max_length=256,null=True,blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=MAINTENANCE_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "device_maintenances"

    def __str__(self):
        return "{}-{}".format(self.user.username, self.device.name)

class Interfaces(CreatedUpdatedModel):
    """Interfaces"""
    INTERFACE_TYPE = (
        ('Rack', 'Rack'),
        ('PowerOutlet', 'PowerOutlet'),
        ('Network', 'Network'),
        ('Console', 'Console'),
        ('USB', 'USB'),
    )

    INTERFACE_STATUS = (
        ('Idle', 'Idle'),
        ('Running', 'Running'),
        ('Deprecated', 'Deprecated'),
        ('Invalid', 'Invalid'),
    )

    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    device = models.ForeignKey(Devices, related_name='interfaces', on_delete=models.CASCADE)
    tag = models.CharField(max_length=128,null=True,blank=True)
    type = models.CharField(max_length=32, choices=INTERFACE_TYPE)
    name = models.CharField(max_length=256,null=True,blank=True)
    index = models.PositiveSmallIntegerField('Interface Index', null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=INTERFACE_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "interfaces"

    def __str__(self):
        return self.name

class InterfaceRacks(Interfaces):
    """Rack Interfaces"""
    has_rail = models.NullBooleanField()
    rail_model = models.CharField(max_length=256,null=True,blank=True)

    class Meta:
        db_table = "interface_racks"

    def __str__(self):
        return self.name

class InterfaceNetworks(Interfaces):
    """Network Interfaces"""
    NETWORK_PORT_MODEL = (
        ('Trunk', 'Trunk'),
        ('Access', 'Access'),
    )

    NETWORK_PORT_TYPE = (
        ('Ethernet', 'Ethernet'),
        ('Fiber', 'Fiber'),
    )

    port_model = models.CharField(max_length=32, choices=NETWORK_PORT_MODEL, null=True, blank=True)
    port_fast = models.NullBooleanField()
    port_type = models.CharField(max_length=32, choices=NETWORK_PORT_TYPE, null=True, blank=True)
    speed = models.PositiveIntegerField(null=True, blank=True)
    mac = models.CharField(max_length=128, verbose_name='MAC Address', null=True, blank=True)

    class Meta:
        db_table = "interface_networks"

    def __str__(self):
        return self.name

class Connections(CreatedUpdatedModel):
    """Connections"""
    CONNECTION_TYPE = (
        ('Rack', 'Rack'),
        ('PowerOutlet', 'PowerOutlet'),
        ('Network', 'Network'),
        ('Console', 'Console'),
        ('USB', 'USB'),
    )

    CONNECTION_STATUS = (
        ('Reserved', 'Reserved'),
        ('Running', 'Running'),
        ('Deprecated', 'Deprecated'),
    )

    interface_a = models.ForeignKey(Interfaces, related_name='interface_a', on_delete=models.SET_NULL, blank=True, null=True)
    interface_b = models.ForeignKey(Interfaces, related_name='interface_b', on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=32, choices=CONNECTION_TYPE)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=CONNECTION_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "connections"

    def __str__(self):
        if self.interface_a or self.interface_b:
            return "{}-{}-{}".format(self.type,self.interface_a.name,self.interface_b.name)
        else:
            return self.type

