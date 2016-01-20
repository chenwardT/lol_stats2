# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_bucket_is_exact_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='total_assists',
            new_name='sum_assists',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_bans',
            new_name='sum_bans',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_damage_dealt',
            new_name='sum_damage_dealt',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_damage_taken',
            new_name='sum_damage_taken',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_deaths',
            new_name='sum_deaths',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_enemy_jungle_cs',
            new_name='sum_enemy_jungle_cs',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_gold_earned',
            new_name='sum_gold_earned',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_killing_sprees',
            new_name='sum_kills',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_kills',
            new_name='sum_largest_killing_spree',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_losses',
            new_name='sum_losses',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_minions_killed',
            new_name='sum_minions_killed',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_picks',
            new_name='sum_picks',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_self_healing',
            new_name='sum_self_healing',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_team_jungle_cs',
            new_name='sum_team_jungle_cs',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='total_wins',
            new_name='sum_wins',
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_assists',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_damage_dealt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_damage_taken',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_death',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_enemy_jungle_cs',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_gold_earned',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_kills',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_largest_killing_spree',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_minions_killed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_pick_count',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_self_healing',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_team_jungle_cs',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='pick_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='win_rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
