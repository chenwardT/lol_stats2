# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0004_auto_20150612_1532'),
        ('matches', '0003_auto_20150612_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='participant_identity',
        ),
        migrations.AddField(
            model_name='participantidentity',
            name='player',
            field=models.ForeignKey(to='summoners.Summoner', default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
