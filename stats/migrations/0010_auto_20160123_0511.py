# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_auto_20160120_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championstats',
            old_name='avg_death',
            new_name='avg_deaths',
        ),
    ]
