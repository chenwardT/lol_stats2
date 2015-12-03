# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0008_auto_20151118_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='last_full_update',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
