# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-19 02:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20181019_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='conference',
        ),
    ]
