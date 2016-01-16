# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20160116_0024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='total_team_jugnle_cs',
            new_name='total_team_jungle_cs',
        ),
    ]
