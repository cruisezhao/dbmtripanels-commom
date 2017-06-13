from django.db import models
from common.utilities.utils import uuid_to_str
from common.apps.product.models import Product, Plan


ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Active','Active'),
    ('Cancelled','Cancelled'),
    ('Invalid','Invalid'),
)

class Orders(models.Model):
    """Orders"""
    uuid = models.CharField(db_index=True, default=uuid_to_str, max_length=255, editable=False)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan,on_delete=models.PROTECT)
    amount = models.DecimalField('Total Fee', max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=32, choices=ORDER_STATUS)
    comment = models.TextField('Comment', max_length=2048, null=True, blank=True)
    notes = models.TextField('Note', max_length=2048, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ['-created_date']
