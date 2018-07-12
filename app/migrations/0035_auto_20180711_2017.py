# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-11 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20180711_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='index',
            name='slide3descrb',
            field=models.CharField(default=django.utils.timezone.now, max_length=300, verbose_name=b'Slide3 description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='index',
            name='slide3head',
            field=models.CharField(default=django.utils.timezone.now, max_length=300, verbose_name=b'Slide3 header'),
            preserve_default=False,
        ),
    ]
