# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stlsite', '0023_auto_20170407_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='repeater',
            name='destination',
            field=models.IntegerField(default=0),
        ),
    ]
