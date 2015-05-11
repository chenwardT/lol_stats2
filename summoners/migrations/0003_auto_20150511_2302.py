# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0002_auto_20150511_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='summoner_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='summoner',
            unique_together=set([('summoner_id', 'region')]),
        ),
    ]
