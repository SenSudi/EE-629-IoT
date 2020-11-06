# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 05:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_scratchpad'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tester',
            name='scratch_pad',
        ),
        migrations.AddField(
            model_name='tester',
            name='scratchpad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.Scratchpad'),
        ),
    ]
