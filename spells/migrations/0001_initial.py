# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('spell_id', models.IntegerField(primary_key=True, serialize=False)),
                ('summoner_level', models.IntegerField()),
                ('name', models.CharField(max_length=16)),
                ('key', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
    ]
