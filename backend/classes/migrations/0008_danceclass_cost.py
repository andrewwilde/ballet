# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-02 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0007_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
