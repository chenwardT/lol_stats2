# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20160116_0221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='ban_count',
            new_name='total_bans',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='loss_count',
            new_name='total_losses',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='pick_count',
            new_name='total_picks',
        ),
        migrations.RenameField(
            model_name='championstats',
            old_name='win_count',
            new_name='total_wins',
        ),
    ]
