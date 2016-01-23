# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_auto_20160123_0515'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='championstats',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='championstats',
            name='champion_id',
        ),
    ]
