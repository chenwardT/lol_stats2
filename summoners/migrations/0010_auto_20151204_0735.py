# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0009_summoner_last_full_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvalidSummonerQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('region', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='invalidsummonerquery',
            unique_together=set([('name', 'region')]),
        ),
    ]
