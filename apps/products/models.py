from django.db import models
from common.utilities.utils import uuid_to_str
from common.utilities.models import CreatedUpdatedModel
from jsonfield import fields

from django.conf import settings
from crum import get_current_user

PENDING_STATUS = 1
ACTIVE_STATUS = 2
SUSPENDED_STATUS = 3
CANCELLED_STATUS = 4

STATUS_CHOICES  = (
        (1,'Pending'),
        (2,'Active'),
        (3,'Suspended'),
        (4,'Cancelled'),
)

class Products(CreatedUpdatedModel):
    """product model"""
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 256, unique = True, db_index = True)
    type = models.CharField('Type', max_length=32, null=False, blank=False)
    name = models.CharField('Name', max_length=255, unique=True)
    summary = models.TextField('Summary', null=True, blank=True)
    description = models.TextField('Description',null=True, blank=True)
    software_url = models.URLField('Software URL', max_length=256, null=True, blank=True)
    software_pic = models.CharField('Software Logo', max_length=255, null=True, blank=True)
    software_img = models.CharField("Software Img", max_length=255, null=True, blank=True)
    vendor_name = models.CharField('Vendor Name',max_length=256,null=True, blank=True)
    vendor_url = models.URLField('Vendor URL',max_length=256,null=True, blank=True)
    latest_version = models.CharField('Latest Version', max_length=256, null=True, blank=True)
    latest_release_date = models.DateTimeField('Latest Release Date', null=True, blank=True)
    opensource = models.BooleanField('OpenSource', default=True)
    license_type = models.CharField('License Type', max_length=256, null=True, blank=True)
    demo_url = models.URLField('Demo URL', max_length=256, null=True, blank=True)
    demo_version = models.CharField('Demo Version', max_length=256,null=True, blank=True)
    facebook_url  = models.URLField('Facebook URL', max_length=256,null=True, blank=True)
    google_plus_url = models.URLField('Googke Plus URL', max_length=256, null=True, blank=True)
    linkedin_url = models.URLField('Linked In URL', max_length=256, null=True, blank=True)
    twitter_url  = models.URLField('Twitter URL',max_length=256, null=True, blank=True)
    document_url = models.URLField('Document URL', max_length=256, null=True, blank=True)
    total_users = models.IntegerField("Total Users", default=0)
    free_plan = models.URLField('Free Plan', max_length=256, null=True, blank=True)
    free_plan_spec =  models.CharField('Free PlanSpec',max_length=256,null=True, blank=True)
    paid_plan = models.URLField('Paid Plan', max_length=256, null=True, blank=True)
    paid_plan_price = models.DecimalField('Paid PlanPrice', max_digits=19, decimal_places=4, null=True, blank=True)
    paid_plan_spec = models.CharField('Paid PlanSpec', max_length=256, null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    features = fields.JSONField('Features', default={})
    in_homepage = models.BooleanField('Showinhomepage', default=False, blank=True)
    created_by = models.CharField('Created By', max_length=256,null=True, blank=True)
    updated_by = models.CharField('Updated By', max_length=256,null=True, blank=True)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"
        db_table = "products"

    def __str__(self):
        return self.name


class ProductApps(CreatedUpdatedModel):
    """software app"""
    product = models.OneToOneField(Products, primary_key=True)

    class Meta:
        verbose_name = "ProductApps"
        verbose_name_plural = "ProductApps"
        db_table = "product_apps"

    def __str__(self):
        return "{}_{}".format(self.product.type,self.product.name)


class ProductVms(CreatedUpdatedModel):
    """vm model"""
    product = models.OneToOneField(Products, primary_key=True)

    class Meta:
        verbose_name = "ProductVms"
        verbose_name_plural = "ProductVms"
        db_table = "product_vms"

    def __str__(self):
        return "{}_{}".format(self.product.type, self.product.name)


class ProductBares(CreatedUpdatedModel):
    """bare product"""
    product = models.OneToOneField(Products, primary_key=True)

    class Meta:
        verbose_name = "ProductBares"
        verbose_name_plural = "ProductBares"
        db_table = "product_bares"

    def __str__(self):
        return "{}_{}".format(self.product.type, self.product.name)


class Screenshot(CreatedUpdatedModel):
    """software screen shot"""
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 256, unique = True, db_index = True)
    product = models.ForeignKey(Products)
    version = models.CharField('Version', max_length=32, null=True, blank=True)
    title = models.CharField('Title', max_length=32, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    url  = models.URLField('URL', max_length=256,null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    created_by = models.CharField('Created By', max_length=256, null=True, blank=True)
    updated_by = models.CharField('Updated By', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Screenshots"
        verbose_name_plural = "Screenshots"
        db_table = "screenshots"


class Review(CreatedUpdatedModel):
    """review for software"""
    RATING_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    )

    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 256, unique = True, db_index = True)
    product = models.ForeignKey(Products)
    rating = models.IntegerField('Rating',default=5, choices=RATING_CHOICES)
    reviews = models.TextField('Review',null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, related_name='rcu')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, related_name='ruu')

    def __str__(self):
        return "{}-{}".format(self.product.name, self.created_by.name)

    class Meta:
        verbose_name = "Reviews"
        verbose_name_plural = "Reviews"
        db_table = "reviews"


class Video(CreatedUpdatedModel):
    """video for software"""
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 256, unique = True, db_index = True)
    product = models.ForeignKey(Products)
    title = models.CharField('Title', max_length=32, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    url  = models.URLField('URL', max_length=256,null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    created_by = models.CharField('Created By', max_length=256, null=True, blank=True)
    updated_by = models.CharField('Updated By', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Videos"
        verbose_name_plural = "Videos"
        db_table = "videos"