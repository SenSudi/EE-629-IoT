# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 05:33
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20161224_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tester',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to=users.models.user_directory_path),
        ),
    ]
