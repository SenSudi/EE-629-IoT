# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-06 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('methodologies', '0025_project_type_sequence'),
    ]

    operations = [
        migrations.CreateModel(
            name='Method_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField(default=1)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='methodologies.Method')),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='methodologies.Phase')),
                ('project_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='methodologies.Project_Type')),
            ],
        ),
    ]
