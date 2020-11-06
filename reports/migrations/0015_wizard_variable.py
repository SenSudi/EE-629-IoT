# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('reports', '0014_wizard_step_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wizard_Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(blank=True, max_length=260, null=True)),
                ('lineage_guid', models.CharField(blank=True, max_length=260, null=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('limit', models.PositiveIntegerField(default=1000)),
                ('input_type', models.CharField(blank=True, max_length=100, null=True)),
                ('multiple', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
