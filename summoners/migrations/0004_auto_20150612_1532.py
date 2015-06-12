# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0003_auto_20150511_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='revision_date',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='summoner_level',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
