# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-30 17:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='magic_token_ttl',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 30, 17, 28, 32, 657293, tzinfo=utc)),
        ),
    ]
