# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-28 11:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0012_hash_nfc_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tos_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
