# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('version', models.CharField(max_length=16)),
                ('region', models.CharField(max_length=8)),
                ('role', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionStats',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('champion_id', models.IntegerField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('pick_count', models.BigIntegerField()),
                ('ban_count', models.BigIntegerField()),
                ('win_count', models.BigIntegerField()),
                ('win_rate', models.IntegerField()),
                ('loss_count', models.BigIntegerField()),
                ('pick_rate', models.IntegerField()),
                ('avg_pick_count', models.IntegerField()),
                ('total_kills', models.BigIntegerField()),
                ('avg_kills', models.IntegerField()),
                ('total_deaths', models.BigIntegerField()),
                ('avg_death', models.IntegerField()),
                ('total_assists', models.BigIntegerField()),
                ('avg_assists', models.IntegerField()),
                ('total_killing_sprees', models.BigIntegerField()),
                ('avg_largest_killing_spree', models.IntegerField()),
                ('total_damage_dealt', models.BigIntegerField()),
                ('avg_damage_dealt', models.IntegerField()),
                ('total_damage_taken', models.BigIntegerField()),
                ('avg_damage_taken', models.IntegerField()),
                ('total_self_healing', models.BigIntegerField()),
                ('avg_self_healing', models.IntegerField()),
                ('total_minions_killed', models.BigIntegerField()),
                ('avg_minions_killed', models.IntegerField()),
                ('total_enemy_jungle_cs', models.BigIntegerField()),
                ('avg_enemy_jungle_cs', models.IntegerField()),
                ('total_team_jugnle_cs', models.BigIntegerField()),
                ('avg_team_jungle_cs', models.IntegerField()),
                ('total_gold_earned', models.BigIntegerField()),
                ('avg_gold_earned', models.IntegerField()),
                ('role_position', models.IntegerField()),
                ('position_delta', models.IntegerField()),
                ('bucket', models.ForeignKey(to='stats.Bucket')),
            ],
        ),
    ]
