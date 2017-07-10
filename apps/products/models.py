from django.db import models
from common.utilities.utils import uuid_to_str
from common.utilities.models import CreatedUpdatedModel
from jsonfield import fields
import random

from django.conf import settings
from crum import get_current_user
from django.urls.base import reverse

PENDING_STATUS = 1
ACTIVE_STATUS = 2
SUSPENDED_STATUS = 3
CANCELLED_STATUS = 4

STATUS_CHOICES  = [
        (1,'Pending'),
        (2,'Active'),
        (3,'Suspended'),
        (4,'Cancelled'),
]


class Plans(CreatedUpdatedModel):
    """create plan model"""
    CHOICE = [3.18, 4.18, 5.18, 15.18, 20.18]
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 255, unique = True)
    name = models.CharField('Name', max_length = 32)
    cpu = models.IntegerField('CPU',default=random.choice(range(4)))
    cpu_description = models.CharField('CPU Description', max_length = 256, null = True, blank = True)
    memory = models.DecimalField('Memory', max_digits=19, decimal_places=2, null=True, blank=True, default=random.choice(range(8)))
    memory_description = models.CharField('Memory Description', max_length = 256, null = True, blank = True)
    disk = models.IntegerField('Disk', default = random.choice(range(4)))
    disk_description = models.CharField('Disk Description', max_length = 256, null = True, blank = True)
    instance = models.IntegerField('Instance', default = random.randint(1,4))
    instance_description = models.CharField('Instance Description', max_length = 256, null = True, blank = True)
    description = models.CharField('Descriptin', max_length = 256, null = True, blank = True)
    price = models.DecimalField('Price',max_digits=19, decimal_places=2, null=True, blank=True, default = random.choice(CHOICE))

    class Meta:
        verbose_name = "Plans"
        verbose_name_plural = "Plans"
        db_table = "plans"

    def __str__(self):
        return self.name


class Products(CreatedUpdatedModel):
    """product model"""
    TYPE_CHOICE = [
        ('APP', 'APP'),
        ('VM', 'VM'),
        ('BARE', 'BARE'),
    ]
    plans = models.ManyToManyField(Plans, blank=True)
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 255, unique = True, db_index = True)
    product_type = models.CharField('Type', max_length=32, default=TYPE_CHOICE[0], choices=TYPE_CHOICE)
    product_name = models.CharField('Name', max_length=255, unique=True)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"
        db_table = "products"

    @property
    def all_plans(self):

        return ', '.\
            join(
            ['<a href="/plan/{}/">{}</a>'.format(p.uuid, p.name) for p in self.plans.all()]
                 )

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product', args=[self.uuid])

    @property
    def get_model(self):
        """get apps\bare\vm model according product_type """
        if self.product_type == self.TYPE_CHOICE[0][0]:
            try:
                return self.productapps
            except ProductApps.DoesNotExist:
                return None
        elif self.product_type == self.TYPE_CHOICE[1][0]:
            try:
                return self.productvms
            except ProductVms.DoesNotExist:
                return None
        else:
            try:
                return self.productbares
            except ProductBares.DoesNotExist:
                return None


class ProductApps(CreatedUpdatedModel):
    """software app"""
    product = models.OneToOneField(Products, primary_key=True)
    app_name = models.CharField('Name', max_length=255, unique=True)
    summary = models.TextField('Summary', null=True, blank=True)
    description = models.TextField('Description',null=True, blank=True)
    product_url = models.URLField('Product URL', max_length=256, null=True, blank=True)
    product_pic = models.CharField('Product Logo', max_length=255, null=True, blank=True)
    product_img = models.CharField("Product Img", max_length=255, null=True, blank=True)
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
    paid_plan_price = models.DecimalField('Paid PlanPrice', max_digits=19, decimal_places=2, null=True, blank=True)
    paid_plan_spec = models.CharField('Paid PlanSpec', max_length=256, null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    features = fields.JSONField('Features', default={})
    environments = fields.JSONField('Environments', default={})
    in_homepage = models.BooleanField('Showinhomepage', default=False, blank=True)
    created_by = models.CharField('Created By', max_length=256,null=True, blank=True)
    updated_by = models.CharField('Updated By', max_length=256,null=True, blank=True)

    class Meta:
        verbose_name = "ProductApps"
        verbose_name_plural = "ProductApps"
        db_table = "product_apps"

    def __str__(self):
        return self.app_name

    def get_product_uuid(self):
        return self.product.uuid

    def get_screenshots(self):
        """return productapp related screenshot"""
        screenshots = Screenshot.objects.filter(product=self)
        dict_screenshots = dict(zip([s.id for s in screenshots],[s.url for s in screenshots]))
        return dict_screenshots

    def get_videos(self):
        """return productapp related video"""
        screenshots = Video.objects.filter(product=self)
        dict_screenshots = dict(zip([s.id for s in screenshots],[s.url for s in screenshots]))
        return dict_screenshots


class ProductVms(CreatedUpdatedModel):
    """vm model"""
    product = models.OneToOneField(Products, primary_key=True)

    class Meta:
        verbose_name = "ProductVms"
        verbose_name_plural = "ProductVms"
        db_table = "product_vms"

    def __str__(self):
        return self.product.product_name


class ProductBares(CreatedUpdatedModel):
    """bare product"""
    product = models.OneToOneField(Products, primary_key=True)

    class Meta:
        verbose_name = "ProductBares"
        verbose_name_plural = "ProductBares"
        db_table = "product_bares"

    def __str__(self):
        return self.product.product_name


class Screenshot(CreatedUpdatedModel):
    """software screen shot"""
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 255, unique = True, db_index = True)
    product = models.ForeignKey(ProductApps)
    version = models.CharField('Version', max_length=32, null=True, blank=True)
    title = models.CharField('Title', max_length=256, null=True, blank=True)
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

    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 255, unique = True, db_index = True)
    product = models.ForeignKey(Products)
    rating = models.IntegerField('Rating',default=5, choices=RATING_CHOICES)
    reviews = models.TextField('Review',null=True, blank=True)
    status = models.IntegerField('Status', default=PENDING_STATUS, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, related_name='rcu')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, related_name='ruu')

    def __str__(self):
        return "{}-{}".format(self.product.product_name, self.created_by.name)

    class Meta:
        verbose_name = "Reviews"
        verbose_name_plural = "Reviews"
        db_table = "reviews"


class Video(CreatedUpdatedModel):
    """video for software"""
    uuid = models.CharField('uuid', default=uuid_to_str, editable=False, max_length = 255, unique = True, db_index = True)
    product = models.ForeignKey(ProductApps)
    title = models.CharField('Title', max_length=256, null=True, blank=True)
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