# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-07 20:22
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0029_wizard_variable_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wizard_variable',
            name='selected',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=-1), size=None),
        ),
    ]
