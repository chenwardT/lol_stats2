# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0005_auto_20150710_0407'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='summoner',
            index_together=set([('summoner_id', 'region')]),
        ),
    ]
