# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-31 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stlsite', '0032_order_commendnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='commendNum',
            field=models.CharField(default='1', max_length=100),
        ),
    ]