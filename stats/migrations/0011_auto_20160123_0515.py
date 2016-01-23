# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20160123_0511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_neutral_minions_killed_friendly_jungle',
            new_name='avg_neutral_minions_killed_team_jungle',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_neutral_minions_killed_friendly_jungle',
            new_name='sum_neutral_minions_killed_team_jungle',
        ),
    ]
