# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 05:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_scratchpad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scratchpad',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='current_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
