# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 16:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_music'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Music',
        ),
    ]
