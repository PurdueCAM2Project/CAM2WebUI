# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 19:27
from __future__ import unicode_literals

import app.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auto_20170615_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applist', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='history',
            name='month',
            field=models.PositiveIntegerField(validators=[app.validators.validateMonth]),
        ),
        migrations.AlterField(
            model_name='history',
            name='year',
            field=models.PositiveIntegerField(validators=[app.validators.validateYear]),
        ),
        migrations.AlterField(
            model_name='leader',
            name='leaderimg',
            field=models.CharField(max_length=300, validators=[app.validators.validateURL], verbose_name='Leader Image'),
        ),
        migrations.AlterField(
            model_name='leader',
            name='leadername',
            field=models.CharField(max_length=50, validators=[app.validators.validateName], verbose_name='Leader Name'),
        ),
        migrations.AlterField(
            model_name='leader',
            name='leaderpagelink',
            field=models.CharField(blank=True, max_length=300, null=True, validators=[app.validators.validateURL], verbose_name='Leader Page Link (Optional)'),
        ),
        migrations.AlterField(
            model_name='member',
            name='memberimg',
            field=models.CharField(blank=True, max_length=300, null=True, validators=[app.validators.validateURL], verbose_name='Member Image'),
        ),
        migrations.AlterField(
            model_name='member',
            name='membername',
            field=models.CharField(max_length=50, validators=[app.validators.validateName], verbose_name='Member Name'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='paperlink',
            field=models.CharField(blank=True, max_length=300, null=True, validators=[app.validators.validateURL], verbose_name='Publication Paper Link (Optional)'),
        ),
        migrations.AlterField(
            model_name='team',
            name='teamimg',
            field=models.CharField(max_length=300, validators=[app.validators.validateURL], verbose_name='Team Image'),
        ),
    ]
