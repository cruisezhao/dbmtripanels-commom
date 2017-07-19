from django.db import models
from .util import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from .network import DataCenters, Interfaces

VLAN_STATUS = (
    ('USED','used'),
    ('UNUSED', 'unused'),
)

AF_CHOICES = (
    (4, 'IPv4'),
    (6, 'IPv6'),
)

PREFIX_STATUS = (
    ('CONTAINER', 'Container'),
    ('ACTIVE', 'Active'),
    ('RESERVED', 'Reserved'),
    ('DEPRECATED', 'Deprecated')
)

PREFIX_TYPE = (
    ('PRIVATE', 'private'),
    ('PUBLIC', 'public'),
    ('MANAGEMENT', 'management'),
)

IPADDRESS_STATUS = (
    ('ACTIVE', 'Active'),
    ('RESERVED', 'Reserved'),
    ('DEPRECATED', 'Deprecated'),
    ('DHCP', 'DHCP')
)

IPADDRESS_TYPE = (
    ('PRIVATE', 'private'),
    ('PUBLIC', 'public'),
    ('MANAGEMENT', 'management'),
)

class VLANs(CreatedUpdatedModel):
    """VLANs"""
    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64)
    vid = models.PositiveSmallIntegerField(verbose_name='VLAN ID')
    status = models.CharField(max_length=64, choices=VLAN_STATUS)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "vlans"

class Prefixes(CreatedUpdatedModel):
    """IP Prefixes"""
    family = models.PositiveSmallIntegerField(choices=AF_CHOICES, editable=False)
    prefix = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    data_center = models.ForeignKey(DataCenters, models.SET_NULL, null=True, blank=True)
    vlan = models.ForeignKey(VLANs, models.SET_NULL, blank=True, null=True, verbose_name='VLAN')
    status = models.CharField(max_length=64, choices=PREFIX_STATUS)
    type = models.CharField(max_length=64, choices=PREFIX_TYPE)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "prefixes"

class IPAddresses(CreatedUpdatedModel):
    """IP Addresses"""
    family = models.PositiveSmallIntegerField(choices=AF_CHOICES, editable=False)
    address = models.GenericIPAddressField(protocol='both', help_text="IPv4 or IPv6 network with mask")
    prefix =  models.ForeignKey(Prefixes, models.SET_NULL, blank=True, null=True, verbose_name='PREFIX')
    interface = models.ForeignKey(Interfaces, related_name='ip_addresses', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=64, choices=IPADDRESS_STATUS)
    type = models.CharField(max_length=64, choices=IPADDRESS_TYPE)
    # nat_inside = models.OneToOneField('self', related_name='nat_outside', on_delete=models.SET_NULL, blank=True,
    #                                   null=True, verbose_name='NAT (Inside)',
    #                                   help_text="The IP for which this address is the \"outside\" IP")
    description = models.TextField(blank=True)

    class Meta:
        db_table = "ip_addresses"


