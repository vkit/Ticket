# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-11 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('street', '0016_userprofile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='allow_notification',
            field=models.IntegerField(blank=True, default=1, help_text='0-OFF,1-ON', null=True),
        ),
    ]
