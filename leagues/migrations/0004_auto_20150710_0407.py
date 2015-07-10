# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0003_league_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='region',
            field=models.CharField(db_index=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='leagueentry',
            name='player_or_team_id',
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
