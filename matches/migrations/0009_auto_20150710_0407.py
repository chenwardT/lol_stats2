# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_auto_20150623_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchdetail',
            name='match_id',
            field=models.BigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='matchdetail',
            name='region',
            field=models.CharField(db_index=True, max_length=4),
        ),
    ]
