# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-24 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_auto_20170524_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='wizard_step',
            name='sequence',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]
