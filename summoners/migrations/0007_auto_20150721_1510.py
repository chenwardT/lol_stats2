# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0006_auto_20150715_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='last_leagues_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='summoner',
            name='last_matches_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
