# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_project_contract_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='completion_milestone', to='project.Milestone'),
        ),
    ]
