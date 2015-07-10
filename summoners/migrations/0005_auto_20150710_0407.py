# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0004_auto_20150612_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='region',
            field=models.CharField(db_index=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='std_name',
            field=models.CharField(db_index=True, max_length=24),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='summoner_id',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
