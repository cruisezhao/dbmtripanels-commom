# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-05 01:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0012_queue_default_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticketcustomfieldvalue',
            unique_together=set([('ticket', 'field')]),
        ),
    ]