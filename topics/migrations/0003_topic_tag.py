# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20160628_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='tag',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
