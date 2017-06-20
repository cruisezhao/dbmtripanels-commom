from django.db import models
from common.utilities.utils import uuid_to_str
from common.apps.products.models import Products, Plans
from common.apps.clients.models import Clients
from common.apps.packages.models import Packages


ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Active','Active'),
    ('Cancelled','Cancelled'),
    ('Invalid','Invalid'),
)

class Orders(models.Model):
    """Orders"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    client = models.ForeignKey(Clients,on_delete=models.PROTECT)
    product = models.ForeignKey(Products,on_delete=models.PROTECT)
    plan = models.ForeignKey(Plans,on_delete=models.PROTECT)
    package = models.ForeignKey(Packages, models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField('Total Fee', max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=32, choices=ORDER_STATUS)
    comment = models.TextField('Comment', max_length=2048, null=True, blank=True)
    notes = models.TextField('Notes', max_length=2048, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ['-created_date']
    
    def get_user_email(self):
        return self.package.client.email
    
    def get_product_name(self):
        return self.product.name
    
    def get_package_name(self):
        if self.package:
            return self.package.get_name()
        else:
            return ''
        
    def get_user_remarks(self):
        return self.comment
    
    def get_plan_name(self):
        return self.plan.name
         
    def get_product_version(self):
        return self.product.productapps.latest_version
    
    def get_product_pic_path(self):
        return self.product.productapps.product_pic
    
    def get_cpu_cores(self):
        return self.plan.cpu
    
    def get_memory(self):
        return self.plan.memory

    def get_disks(self):
        return self.plan.disk
    
    def get_bandwidth(self):
        return ''