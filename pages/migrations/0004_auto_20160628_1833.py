# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_pagetopic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='last_scan',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last scanned'),
        ),
    ]
