# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-24 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_auto_20180923_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='subteam',
            field=models.CharField(blank=True, choices=[(b'I', b'Image Analysis'), (b'UI', b'Web UI'), (b'D+API', b'API team'), (b'PP', b'Parrellel Perforamce'), (b'RM', b'Reserouce Management'), (b'SE', b'Software Engineering'), (b'MA', b'Mobile App'), (b'CR', b'Camera Reliability'), (b'CD', b'Camera Discovery'), (b'CData', b'Camera Database'), (b'TL', b'Transfer Learning'), (b'AT', b'Active Training'), (b'ID', b'Image Database'), (b'DV', b'Drone Video'), (b'FIA', b'Forest Inventory Analysis'), (b'HB', b'Human Behavior'), (b'CS', b'Crowdsourcing'), (b'Intel', b'Embedded Computer Vision')], default=b'blank', max_length=50, verbose_name=b'Subteam'),
        ),
    ]
