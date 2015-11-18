# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0009_auto_20150710_0407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchdetail',
            options={'get_latest_by': 'match_creation'},
        ),
    ]
