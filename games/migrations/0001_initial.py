# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0001_initial'),
        ('summoners', '0003_auto_20150511_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('create_date', models.BigIntegerField()),
                ('game_id', models.BigIntegerField()),
                ('game_mode', models.CharField(max_length=16)),
                ('game_type', models.CharField(max_length=16)),
                ('invalid', models.BooleanField()),
                ('ip_earned', models.IntegerField()),
                ('level', models.IntegerField()),
                ('map_id', models.IntegerField()),
                ('spell_1', models.IntegerField()),
                ('spell_2', models.IntegerField()),
                ('sub_type', models.CharField(max_length=24)),
                ('team_id', models.IntegerField()),
                ('region', models.CharField(max_length=4)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('champion_key', models.CharField(max_length=32)),
                ('champion_id', models.ForeignKey(to='champions.Champion')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('team_id', models.IntegerField()),
                ('champion', models.ForeignKey(to='champions.Champion')),
                ('participant_of', models.ForeignKey(to='games.Game')),
                ('summoner', models.ForeignKey(to='summoners.Summoner')),
            ],
            options={
                'ordering': ('team_id',),
            },
        ),
        migrations.CreateModel(
            name='RawStat',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('assists', models.IntegerField(null=True, blank=True)),
                ('barracks_killed', models.IntegerField(null=True, blank=True)),
                ('champions_killed', models.IntegerField(null=True, blank=True)),
                ('combat_player_score', models.IntegerField(null=True, blank=True)),
                ('consumables_purchased', models.IntegerField(null=True, blank=True)),
                ('damage_dealt_player', models.IntegerField(null=True, blank=True)),
                ('double_kills', models.IntegerField(null=True, blank=True)),
                ('first_blood', models.IntegerField(null=True, blank=True)),
                ('gold', models.IntegerField(null=True, blank=True)),
                ('gold_earned', models.IntegerField(null=True, blank=True)),
                ('gold_spent', models.IntegerField(null=True, blank=True)),
                ('item0', models.IntegerField(null=True, blank=True)),
                ('item1', models.IntegerField(null=True, blank=True)),
                ('item2', models.IntegerField(null=True, blank=True)),
                ('item3', models.IntegerField(null=True, blank=True)),
                ('item4', models.IntegerField(null=True, blank=True)),
                ('item5', models.IntegerField(null=True, blank=True)),
                ('item6', models.IntegerField(null=True, blank=True)),
                ('items_purchased', models.IntegerField(null=True, blank=True)),
                ('killing_sprees', models.IntegerField(null=True, blank=True)),
                ('largest_critical_strike', models.IntegerField(null=True, blank=True)),
                ('largest_killing_spree', models.IntegerField(null=True, blank=True)),
                ('largest_multi_kill', models.IntegerField(null=True, blank=True)),
                ('legendary_items_created', models.IntegerField(null=True, blank=True)),
                ('level', models.IntegerField(null=True, blank=True)),
                ('magic_damage_dealt_player', models.IntegerField(null=True, blank=True)),
                ('magic_damage_dealt_to_champions', models.IntegerField(null=True, blank=True)),
                ('magic_damage_taken', models.IntegerField(null=True, blank=True)),
                ('minions_denied', models.IntegerField(null=True, blank=True)),
                ('minions_killed', models.IntegerField(null=True, blank=True)),
                ('neutral_minions_killed', models.IntegerField(null=True, blank=True)),
                ('neutral_minions_killed_enemy_jungle', models.IntegerField(null=True, blank=True)),
                ('neutral_minions_killed_your_jungle', models.IntegerField(null=True, blank=True)),
                ('nexus_killed', models.NullBooleanField()),
                ('node_capture', models.IntegerField(null=True, blank=True)),
                ('node_capture_assist', models.IntegerField(null=True, blank=True)),
                ('node_neutralize', models.IntegerField(null=True, blank=True)),
                ('node_neutralize_assist', models.IntegerField(null=True, blank=True)),
                ('num_deaths', models.IntegerField(null=True, blank=True)),
                ('num_items_bought', models.IntegerField(null=True, blank=True)),
                ('objective_player_score', models.IntegerField(null=True, blank=True)),
                ('penta_kills', models.IntegerField(null=True, blank=True)),
                ('physical_damage_dealt_player', models.IntegerField(null=True, blank=True)),
                ('physical_damage_dealt_to_champions', models.IntegerField(null=True, blank=True)),
                ('physical_damage_taken', models.IntegerField(null=True, blank=True)),
                ('quadra_kills', models.IntegerField(null=True, blank=True)),
                ('sight_wards_bought', models.IntegerField(null=True, blank=True)),
                ('spell_1_cast', models.IntegerField(null=True, blank=True)),
                ('spell_2_cast', models.IntegerField(null=True, blank=True)),
                ('spell_3_cast', models.IntegerField(null=True, blank=True)),
                ('spell_4_cast', models.IntegerField(null=True, blank=True)),
                ('summon_spell_1_cast', models.IntegerField(null=True, blank=True)),
                ('summon_spell_2_cast', models.IntegerField(null=True, blank=True)),
                ('super_monster_killed', models.IntegerField(null=True, blank=True)),
                ('team', models.IntegerField(null=True, blank=True)),
                ('team_objective', models.IntegerField(null=True, blank=True)),
                ('time_played', models.IntegerField(null=True, blank=True)),
                ('total_damage_dealt', models.IntegerField(null=True, blank=True)),
                ('total_damage_dealt_to_champions', models.IntegerField(null=True, blank=True)),
                ('total_damage_taken', models.IntegerField(null=True, blank=True)),
                ('total_heal', models.IntegerField(null=True, blank=True)),
                ('total_player_score', models.IntegerField(null=True, blank=True)),
                ('total_score_rank', models.IntegerField(null=True, blank=True)),
                ('total_time_crowd_control_dealt', models.IntegerField(null=True, blank=True)),
                ('total_units_healed', models.IntegerField(null=True, blank=True)),
                ('triple_kills', models.IntegerField(null=True, blank=True)),
                ('true_damage_dealt_player', models.IntegerField(null=True, blank=True)),
                ('true_damage_dealt_to_champions', models.IntegerField(null=True, blank=True)),
                ('true_damage_taken', models.IntegerField(null=True, blank=True)),
                ('turrets_killed', models.IntegerField(null=True, blank=True)),
                ('unreal_kills', models.IntegerField(null=True, blank=True)),
                ('victory_point_total', models.IntegerField(null=True, blank=True)),
                ('vision_wards_bought', models.IntegerField(null=True, blank=True)),
                ('ward_killed', models.IntegerField(null=True, blank=True)),
                ('ward_placed', models.IntegerField(null=True, blank=True)),
                ('win', models.NullBooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='stats',
            field=models.OneToOneField(to='games.RawStat'),
        ),
        migrations.AddField(
            model_name='game',
            name='summoner_id',
            field=models.ForeignKey(to='summoners.Summoner'),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('region', 'game_id', 'summoner_id')]),
        ),
    ]
