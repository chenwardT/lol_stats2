# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0007_auto_20150721_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summoner',
            options={'get_latest_by': 'last_update'},
        ),
    ]
