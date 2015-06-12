# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_auto_20150612_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participantidentity',
            old_name='player',
            new_name='summoner',
        ),
    ]
