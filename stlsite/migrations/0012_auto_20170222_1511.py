# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stlsite', '0011_auto_20170222_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitering',
            name='moniteringTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
