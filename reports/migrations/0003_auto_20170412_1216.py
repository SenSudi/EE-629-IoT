# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20170116_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_item',
            name='description',
            field=models.TextField(),
        ),
    ]
