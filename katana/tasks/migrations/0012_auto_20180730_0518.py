# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-30 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20180730_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='base_command',
            field=models.CharField(blank=True, default='', max_length=3500, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='exec_cmd',
            field=models.TextField(blank=True, default='', max_length=3500, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='exec_duration',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
