# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChampionStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('champion_id', models.IntegerField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('pick_count', models.BigIntegerField()),
                ('ban_count', models.BigIntegerField()),
                ('win_count', models.BigIntegerField()),
                ('loss_count', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='championstats',
            name='version',
            field=models.ForeignKey(to='stats.Version'),
        ),
    ]
