# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('methodologies', '0013_auto_20170310_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='methodologies.Phase'),
        ),
    ]
