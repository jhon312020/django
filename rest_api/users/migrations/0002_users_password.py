# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 14:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default=datetime.datetime(2016, 2, 15, 14, 24, 50, 581000, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
