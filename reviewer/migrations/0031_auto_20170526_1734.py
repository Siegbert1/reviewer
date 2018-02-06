# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0030_auto_20170523_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case_zr',
            old_name='p',
            new_name='cp',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p2',
            new_name='cp2',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p3',
            new_name='cp3',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p4',
            new_name='dp',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p5',
            new_name='dv',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p6',
            new_name='kp',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p7',
            new_name='kp2',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p8',
            new_name='kp3',
        ),
        migrations.RenameField(
            model_name='case_zr',
            old_name='p9',
            new_name='wp',
        ),
        migrations.AddField(
            model_name='case_zr',
            name='wp2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='wp3',
            field=models.BooleanField(default=False),
        ),
    ]