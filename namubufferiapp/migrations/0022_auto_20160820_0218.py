# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 02:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import namubufferiapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0021_auto_20160820_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='magic_hash',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='magic_link_ttl',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='magic_token',
            field=models.CharField(default=namubufferiapp.models.generate_magic_token, max_length=7, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='magic_token_ttl',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 20, 2, 33, 59, 646130, tzinfo=utc)),
        ),
    ]