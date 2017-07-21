from django.db import models
from .util import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from common.apps.users.models import Users

VENDOR_TYPE = (
    ('manufacturer','manufacturer'),
    ('seller', 'seller'),
    ('product_vendor', 'product_vendor'),
    ('cloud_provider', 'cloud_provider'),
)

VENDOR_STATUS = (
    ('USED','used'),
    ('UNUSED', 'unused'),
)

DEVICE_TYPE = (
    ('RACK','rack'),
    ('POWER', 'power'),
    ('DRIVE', 'drive'),
    ('KVM','kvm'),
    ('ROUTER', 'router'),
    ('SWITCH', 'switch'),
    ('FIREWALL', 'firewall'),
    ('BAREMETAL', 'baremetal'),
)

DEVICE_TYPE = (
    ('POWERON','on'),
    ('POWEROFF', 'off'),
)

INTERFACE_TYPE = (
    ('RAIL','rail'),
    ('POWER_OUTLET', 'power_outlet'),
    ('NETWORK', 'network'),
    ('CONSOLE', 'console'),
    ('USB', 'usb'),
)

INTERFACE_STATUS = (
    ('ENABLED','enabled'),
    ('DISABLE', 'disable'),
    ('INVALID', 'invalid'),
    ('ACTIVE', 'active'),
)

MAINTENANCE_STATUS = (
    ('IN_PROCESS','in_process'),
    ('HANG_UP', 'hang_up'),
    ('FINISHED', 'finished'),
)

CONNECTION_TYPE = (
    ('RAIL','rail'),
    ('POWER_OUTLET', 'power_outlet'),
    ('NETWORK', 'network'),
    ('CONSOLE', 'console'),
    ('USB', 'usb'),
)

CONNECTION_STATUS = (
    ('ENABLED','enabled'),
    ('DISABLE', 'disable'),
)

class Vendors(CreatedUpdatedModel):
    """Vendors"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=32, choices=VENDOR_TYPE)
    description = models.CharField(max_length=32)
    website = models.CharField(max_length=64)
    status = models.CharField(max_length=32, choices=VENDOR_STATUS)

    class Meta:
        db_table = "vendors"

    def __str__(self):
        return self.name


class DataCenters(CreatedUpdatedModel):
    """Data Centers"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    zip = models.CharField(max_length=32)
    website = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    support_email = models.CharField(max_length=32)
    support_portal = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    notes = models.CharField(max_length=1024)

    class Meta:
        db_table = "data_centers"

    def __str__(self):
        return self.name


class Devices(CreatedUpdatedModel):
    """Devices"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=32, choices=DEVICE_TYPE)
    manufacturer = models.ForeignKey(Vendors, models.SET_NULL, related_name='manufacturer_device', null=True, blank=True)
    model = models.CharField(max_length=64)
    sn = models.CharField(max_length=50, blank=True, verbose_name='Serial number')
    rack = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Rack')
    u_height = models.PositiveSmallIntegerField(verbose_name='Height In Rack',null=True, blank=True,
                                     help_text='How many rack units does this device occupy')
    tag = models.CharField(max_length=64)
    seller = models.ForeignKey(Vendors, models.SET_NULL, related_name='seller_device', null=True, blank=True)
    purchase_date = models.DateField('Purchase Date', null=True, blank=True)
    price = models.DecimalField('Price',max_digits=10, decimal_places=2)
    order_no = models.CharField(max_length=64)
    warranty_date = models.DateField('Warranty Date', null=True, blank=True)
    status = models.CharField(max_length=32, choices=DEVICE_TYPE)
    comments = models.TextField(blank=True)

    class Meta:
        db_table = "devices"
        ordering = ['-created_date']
        # unique_together = [
        #     ['data_center', 'name'],
        #     ['data_center', 'tag'],
        # ]

    def __str__(self):
        return self.name

class DeviceRacks(Devices):
    """Racks"""
    #desc_units = models.BooleanField(default=False, verbose_name='Descending units',help_text='Units are numbered top-to-bottom')
    location = models.TextField(blank=True, help_text='How to find the rack in data center.')
    total_electric_current = models.CharField(max_length=64)
    used_electric_current = models.CharField(max_length=64)
    ec_check_date = models.DateField('Electric Current Check Date', null=True, blank=True, help_text='Electric Current Check Date')
    power_stripe_amount = models.PositiveSmallIntegerField(null=True, blank=True)
    total_band_width = models.CharField(max_length=64)
    used_band_width = models.CharField(max_length=64)
    bw_check_date = models.DateField('Band Width Check Date', null=True, blank=True, help_text='Band Width Check Date')
    up_router_ip = models.CharField(max_length=255)

    class Meta:
        db_table = "device_racks"

    def __str__(self):
        return self.name

class DevicePowers(Devices):
    """Power Devices"""
    outlet_amount = models.PositiveSmallIntegerField(verbose_name='Power Outlet Amount', null=True, blank=True)
    voltage = models.PositiveSmallIntegerField(verbose_name='Voltage', null=True, blank=True)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)

    class Meta:
        db_table = "device_powers"

    def __str__(self):
        return self.name

class DeviceDrives(Devices):
    """Drives"""
    disk_size = models.CharField(max_length=64)
    file_system = models.CharField(max_length=64)

    class Meta:
        db_table = "device_drives"

    def __str__(self):
        return self.name

class DeviceKVMs(Devices):
    """KVMs"""
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    port_amount = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_kvms"

    def __str__(self):
        return self.name

class DeviceRouters(Devices):
    """Routers"""
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    os_version = models.CharField(max_length=128)
    port_amount = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_routers"

    def __str__(self):
        return self.name

class DeviceSwitches(Devices):
    """Switches"""
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    os_version = models.CharField(max_length=128)
    port_amount = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_switches"

    def __str__(self):
        return self.name

class DeviceFirewalls(Devices):
    """Firewalls"""
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    os_version = models.CharField(max_length=128)
    port_amount = models.PositiveSmallIntegerField(null=True, blank=True)
    license_amount = models.PositiveSmallIntegerField(null=True, blank=True)
    safe_area = models.CharField(max_length=255)
    unsafe_area = models.CharField(max_length=255)

    class Meta:
        db_table = "device_firewalls"

    def __str__(self):
        return self.name

class DeviceBares(Devices):
    """Bare Metals"""
    processor_model = models.CharField(max_length=32)
    no_of_processors = models.PositiveSmallIntegerField('CPU Cores', null=True, blank=True)
    memory_chips = models.CharField(max_length=32)
    memory_size = models.CharField(max_length=32)
    motherboard_model = models.CharField(max_length=32)
    chassis_model = models.CharField(max_length=32)
    power_supply_model = models.CharField(max_length=32)
    disk_size = models.CharField(max_length=32)
    disk_description = models.TextField(blank=True)
    # with_rail = models.NullBooleanField()
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mgmt_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    port_amount = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "device_bares"

    def __str__(self):
        return self.name

class DeviceMaintenances(CreatedUpdatedModel):
    """Device Maintenances"""
    device = models.ForeignKey(Devices)
    user = models.ForeignKey(Users)
    start_time = models.DateTimeField('Start Time', null=True, blank=True)
    end_time = models.DateTimeField('End Time', null=True, blank=True)
    task_subject = models.CharField(max_length=64)
    task_detail = models.CharField(max_length=1024)
    total_minutes = models.PositiveIntegerField('Total Minutes', null=True, blank=True)
    status = models.CharField(max_length=32, choices=MAINTENANCE_STATUS)
    notes = models.CharField(max_length=1024)

    class Meta:
        db_table = "server_maintenances"

    def __str__(self):
        return "{}-{}".format(self.user.name, self.device.name)

class Interfaces(CreatedUpdatedModel):
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    device = models.ForeignKey(Devices, related_name='interfaces', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    type = models.CharField(max_length=32, choices=INTERFACE_TYPE)
    status = models.CharField(max_length=32, choices=INTERFACE_STATUS)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "interfaces"

    def __str__(self):
        return self.name

class InterfaceRacks(Interfaces):
    has_rail = models.NullBooleanField()
    rail_model = models.CharField(max_length=255)
    unit_no = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "racks_interfaces"

    def __str__(self):
        return self.name

class InterfaceNetworks(Interfaces):
    speed = models.CharField(max_length=64)
    mac = models.CharField(max_length=128, null=True, blank=True, verbose_name='MAC Address')
    port_model = models.CharField(max_length=128)

    class Meta:
        db_table = "network_interfaces"

    def __str__(self):
        return self.name

class Connections(CreatedUpdatedModel):
    interface_a = models.ForeignKey(Interfaces, related_name='interface_a', on_delete=models.SET_NULL, blank=True, null=True)
    interface_b = models.ForeignKey(Interfaces, related_name='interface_b', on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=32, choices=CONNECTION_TYPE)
    status = models.CharField(max_length=32, choices=CONNECTION_STATUS)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "connections"

    def __str__(self):
        return "{}-{}-{}".format(self.type,self.interface_a.name,self.interface_b.name)




