# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='participant_of',
            new_name='game',
        ),
        migrations.AddField(
            model_name='rawstat',
            name='player_position',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rawstat',
            name='player_role',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
