# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
