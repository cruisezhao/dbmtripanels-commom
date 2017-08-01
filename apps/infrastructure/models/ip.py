from django.db import models
from .util import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from .network import DataCenters, Interfaces, Devices

class VLANs(CreatedUpdatedModel):
    """VLANs"""
    VLAN_STATUS = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    )

    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(Devices, models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(blank=True)
    vid = models.PositiveSmallIntegerField(verbose_name='VLAN ID')
    status = models.CharField(max_length=32, choices=VLAN_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "vlans"

    def __str__(self):
        return self.name

    def get_device_url(self):
        return "infras:{}".format(self.device.type.lower())


class IPPrefixes(CreatedUpdatedModel):
    """IP Prefixes"""
    AF_CHOICES = (
        ('IPv4', 'IPv4'),
        ('IPv6', 'IPv6'),
    )

    PREFIX_STATUS = (
        ('Container', 'Container'),
        ('Active', 'Active'),
        ('Reserved', 'Reserved'),
        ('Deprecated', 'Deprecated'),
    )

    PREFIX_TYPE = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )

    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(Devices, models.SET_NULL, null=True, blank=True)
    vlan = models.ForeignKey(VLANs, models.SET_NULL, blank=True, null=True, verbose_name='VLAN')
    family = models.CharField(max_length=32, choices=AF_CHOICES)
    type = models.CharField(max_length=64, choices=PREFIX_TYPE)
    prefix = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    notation = models.CharField(max_length=64, null=True, blank=True)
    gateway_ip = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    net_mask = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    description = models.TextField(blank=True)
    start_ip = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    end_ip = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    online_date = models.DateField('Online Date', null=True, blank=True)
    offline_date = models.DateField('Offline Date', null=True, blank=True)
    status = models.CharField(max_length=64, choices=PREFIX_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "ip_prefixes"

class IPAddresses(CreatedUpdatedModel):
    """IP Addresses"""
    IPADDRESS_STATUS = (
        ('Active', 'Active'),
        ('Reserved', 'Reserved'),
        ('Deprecated', 'Deprecated'),
        ('DHCP', 'DHCP'),
    )

    prefix = models.ForeignKey(IPPrefixes, models.SET_NULL, blank=True, null=True, verbose_name='PREFIX')
    address = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    nat_address = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask",blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=IPADDRESS_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "ip_addresses"


class IPInterfaces(CreatedUpdatedModel):
    """IP Interfaces"""
    IP_INTERFACE_STATUS = (
        ('Active', 'Active'),
        ('Reserved', 'Reserved'),
        ('Deprecated', 'Deprecated'),
    )

    interface = models.ForeignKey(Interfaces, on_delete=models.SET_NULL, blank=True, null=True)
    ip = models.ForeignKey(IPAddresses, on_delete=models.SET_NULL, blank=True, null=True)
    allocate_date = models.DateField('Allocate Date', null=True, blank=True)
    revoke_date = models.DateField('Revoke Date', null=True, blank=True)
    status = models.CharField(max_length=32, choices=IP_INTERFACE_STATUS)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "ip_interfaces"



