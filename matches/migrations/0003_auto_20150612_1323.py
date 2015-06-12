# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_auto_20150612_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='participant_stats',
        ),
        migrations.AddField(
            model_name='participant',
            name='assists',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='champ_level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='deaths',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='double_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='first_blood_assist',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='first_blood_kill',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='first_inhibitor_assist',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='first_inhibitor_kill',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='first_tower_assist',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='first_tower_kill',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='gold_earned',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='gold_spent',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='inhibitor_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item0',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item3',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item4',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item5',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='item6',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='killing_sprees',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='largest_critical_strike',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='largest_killing_spree',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='largest_multi_kill',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='magic_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='magic_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='magic_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='minions_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='neutral_minions_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='neutral_minions_killed_enemy_jungle',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='neutral_minions_killed_team_jungle',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='penta_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='physical_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='physical_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='physical_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='quadra_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='sight_wards_bought_in_game',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_heal',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_time_crowd_control_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='total_units_healed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='tower_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='triple_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='true_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='true_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='true_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='unreal_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='vision_wards_bought_in_game',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='wards_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='wards_placed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='winner',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ParticipantStats',
        ),
    ]
