# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-17 03:07
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0016_auto_20180517_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='attr_order',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=['Title']),
        ),
    ]
