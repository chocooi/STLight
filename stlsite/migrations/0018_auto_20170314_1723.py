# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 08:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stlsite', '0017_latlng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zone',
            name='zoneLat',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='zoneLng',
        ),
    ]
