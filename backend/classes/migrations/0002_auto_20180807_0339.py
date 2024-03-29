# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-07 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='class_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='danceclass',
            name='day_of_week',
            field=models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='danceclass',
            name='end_day',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='danceclass',
            name='start_day',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='danceclass',
            name='max_students',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='danceclass',
            name='recital',
            field=models.TextField(default=''),
        ),
    ]
