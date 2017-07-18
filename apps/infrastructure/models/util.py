from django.db import models

class CreatedUpdatedModel(models.Model):
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    created_by = models.PositiveIntegerField('Created By', null=True, blank=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)
    updated_by = models.PositiveIntegerField('Updated Date', null=True, blank=True)

    class Meta:
        abstract = True
