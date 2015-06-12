# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_auto_20150612_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantidentity',
            name='summoner',
            field=models.ForeignKey(null=True, to='summoners.Summoner', blank=True),
        ),
    ]
