# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_lineage_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='newest',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, default='open', max_length=50),
        ),
    ]
