# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-30 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_auto_20181026_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('num_children', models.IntegerField()),
            ],
        ),
    ]
