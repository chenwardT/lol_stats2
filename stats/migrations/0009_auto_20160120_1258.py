# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20160120_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_enemy_jungle_cs',
            new_name='avg_neutral_minions_killed_enemy_jungle',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_team_jungle_cs',
            new_name='avg_neutral_minions_killed_friendly_jungle',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_damage_dealt',
            new_name='avg_total_damage_dealt',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_damage_taken',
            new_name='avg_total_damage_taken',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_self_healing',
            new_name='avg_total_heal',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_enemy_jungle_cs',
            new_name='sum_neutral_minions_killed_enemy_jungle',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_team_jungle_cs',
            new_name='sum_neutral_minions_killed_friendly_jungle',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_damage_dealt',
            new_name='sum_total_damage_dealt',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_damage_taken',
            new_name='sum_total_damage_taken',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='sum_self_healing',
            new_name='sum_total_heal',
        ),
    ]
