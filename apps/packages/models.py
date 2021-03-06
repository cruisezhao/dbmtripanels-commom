# -*- coding:utf-8 -*-

from django.db import models
from common.utilities.models import CreatedUpdatedModel
from common.utilities.utils import uuid_to_str
from django.conf import settings
from common.apps.clients.models import Clients

# Package状态：
# Pending    - ordering a product
# Active      - after pay successfully 
# Suspended   - because of unpaying or abuse
# Cancelled    - cancelled status
# Invalid      - unapproved order

PACKAGE_STATUS= (
    ('Pending','Pending'),
    ('Active', 'Active'),
    ('Suspended','Suspended'),
    ('Cancelled','Cancelled'),
    ('Invalid','Invalid'),
    )


# Create your models here.
class Packages(CreatedUpdatedModel):
    """Packages"""
    DEPLOY_STATUS= (
        ('Undeployed','Undeployed'),
        ('Deploying','Deploying'),
        ('Success', 'Success'),
        ('Failure','Failure'),
        ('Timeout','Timeout'),
    )
    uuid = models.CharField(unique=True, default=uuid_to_str, max_length=255, editable=False)
    package_name = models.CharField(max_length=100)
    description = models.TextField('Description',null=True, blank=True)
    client = models.ForeignKey(Clients,on_delete=models.DO_NOTHING)
    next_due_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    amount = models.DecimalField('Package Fee', max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=32, choices=PACKAGE_STATUS)
    #plan = models.ForeignKey(Plans,on_delete=models.PROTECT)
    #run time content, maybe include : summing all plans 
    #runtime = fields.JSONField('Runtime Information', default={})
    cpu = models.IntegerField('CPU',default=0)
    memory = models.DecimalField('Memory', max_digits=19, decimal_places=4, null=True, blank=True)
    disk = models.IntegerField('Disk', default = 0)
    deploy_status = models.CharField(max_length=32, choices=DEPLOY_STATUS, default='Undeployed')
    
    def is_undeployed(self):
        return self.deploy_status == 'Undeployed'
    
    def allow_to_deploy(self):
        return (self.deploy_status == 'Undeployed') or (self.deploy_status == 'Failure') \
                or (self.deploy_status == 'Timeout')
    
    class Meta:
        db_table = "packages"
    
    def __str__(self):
        return self.package_name
    
    def get_name(self):
        return self.package_name
    
    def get_product_name(self):
        return self.get_product_order().product.product_name
    
    def get_product_id(self):
        return self.get_product_order().product.uuid
    
    def get_product_pic_path(self):
        return self.get_product_order().get_product_pic_path()
    
    
    def get_product_usinginfo(self, appname=''):
        if appname == '':
            app = self.runtime.get("servers")[0].get("applications")[0]
            return (app.get("url", ''), app.get("user_name", ''), app.get("password", ''))
        else:
            #todo: should get infomations based on application name
            return ('', '', '')
        
    def get_plan_name(self):
        return self.get_product_order().plan.name
    
    def get_server_list(self):
        return self.servers_set.all()

    def get_product_order(self):
        return self.orders_set.all()[0]

    def modify_username(self,username):
        self.runtime['servers'][0]['applications'][0]['user_name'] = username

    def modify_password(self,password):
        self.runtime['servers'][0]['applications'][0]['password'] = password

