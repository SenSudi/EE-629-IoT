# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0019_wizard_variable_selectable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_variable',
            name='input_type',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('textarea', 'textarea')], max_length=20, null=True),
        ),
    ]
