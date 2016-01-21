# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0011_auto_20160120_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchdetail',
            name='avg_highest_achieved_season_tier',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
