# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20170103_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
