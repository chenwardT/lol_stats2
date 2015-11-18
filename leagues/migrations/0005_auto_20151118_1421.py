# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_auto_20150710_0407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='league',
            options={'get_latest_by': 'last_update'},
        ),
    ]
