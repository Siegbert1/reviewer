# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-23 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0029_auto_20170522_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='case_zr',
            name='abnahme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='cic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='cicpv',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='cicvm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p5',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p6',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p7',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p8',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='p9',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='wv',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case_zr',
            name='wvmangel',
            field=models.BooleanField(default=False),
        ),
    ]
