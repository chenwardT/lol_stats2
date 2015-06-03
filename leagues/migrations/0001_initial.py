# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('region', models.CharField(max_length=4)),
                ('queue', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('tier', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('division', models.CharField(max_length=3)),
                ('is_fresh_blood', models.BooleanField()),
                ('is_hot_streak', models.BooleanField()),
                ('is_inactive', models.BooleanField()),
                ('is_veteran', models.BooleanField()),
                ('league_points', models.IntegerField()),
                ('player_or_team_id', models.CharField(max_length=64)),
                ('player_or_team_name', models.CharField(max_length=24)),
                ('wins', models.IntegerField()),
                ('series_losses', models.SmallIntegerField(blank=True, null=True)),
                ('series_progress', models.CharField(blank=True, max_length=5, null=True)),
                ('series_target', models.SmallIntegerField(blank=True, null=True)),
                ('series_wins', models.SmallIntegerField(blank=True, null=True)),
                ('league', models.ForeignKey(to='leagues.League')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='league',
            unique_together=set([('region', 'queue', 'name', 'tier')]),
        ),
        migrations.AlterUniqueTogether(
            name='leagueentry',
            unique_together=set([('player_or_team_id', 'league')]),
        ),
    ]
