# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_remove_issue_file_project'),
        ('methodologies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='files',
            field=models.ManyToManyField(blank=True, to='files.Associated_File'),
        ),
    ]
