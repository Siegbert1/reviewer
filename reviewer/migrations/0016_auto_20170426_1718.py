# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0015_category_under_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='under_category',
            new_name='area',
        ),
    ]
