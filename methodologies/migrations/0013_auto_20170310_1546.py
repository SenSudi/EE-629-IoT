# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 20:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('methodologies', '0012_auto_20170310_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='ancestor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='methodologies.Phase'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='descendant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childphase', to='methodologies.Phase'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Project'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='suggestor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
