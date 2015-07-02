# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0002_leagueentry_losses'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 16, 15, 29, 294870), auto_now=True),
            preserve_default=False,
        ),
    ]
