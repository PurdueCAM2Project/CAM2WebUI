# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-21 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_system', '0007_join'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinmodel',
            name='favoriteTeams',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='4 Favorite Teams'),
        ),
    ]
