# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('summoner_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=24)),
                ('std_name', models.CharField(max_length=24)),
                ('profile_icon_id', models.IntegerField()),
                ('revision_date', models.BigIntegerField()),
                ('summoner_level', models.IntegerField()),
                ('region', models.CharField(max_length=4)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
