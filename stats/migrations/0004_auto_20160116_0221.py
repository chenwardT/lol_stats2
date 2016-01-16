# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20160116_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championstats',
            name='avg_assists',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_death',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_enemy_jungle_cs',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_gold_earned',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_largest_killing_spree',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_minions_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_pick_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_self_healing',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='avg_team_jungle_cs',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='ban_count',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='loss_count',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='pick_count',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='pick_rate',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='position_delta',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='role_position',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_assists',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_damage_dealt',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_damage_taken',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_deaths',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_enemy_jungle_cs',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_gold_earned',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_killing_sprees',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_kills',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_minions_killed',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_self_healing',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='total_team_jungle_cs',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='win_count',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='win_rate',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='bucket',
            unique_together=set([('version', 'region', 'lane', 'role')]),
        ),
    ]
