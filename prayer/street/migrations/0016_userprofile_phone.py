# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-11 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('street', '0015_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
