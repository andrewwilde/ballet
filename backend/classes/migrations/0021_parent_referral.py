# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-28 04:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0020_location_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='referral',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]