# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20170310_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='mangle',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
