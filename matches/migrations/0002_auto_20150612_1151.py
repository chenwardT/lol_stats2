# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantstats',
            name='participant',
        ),
        migrations.AddField(
            model_name='participant',
            name='participant_stats',
            field=models.OneToOneField(blank=True, null=True, to='matches.ParticipantStats'),
        ),
    ]
