# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-11 01:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_merge_20181019_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subteam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image_url', models.URLField(blank=True)),
                ('iscurrentmember', models.BooleanField(default=True, verbose_name='Is Current Member')),
                ('isdirector', models.BooleanField(default=False, verbose_name='Is he/she a Director?')),
                ('subteam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Subteam')),
            ],
        ),
    ]
