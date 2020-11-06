# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_tester_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tester',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Project'),
        ),
    ]
