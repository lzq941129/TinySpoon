# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('childrenrecipe', '0004_auto_20160917_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_tag',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
