# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_auto_20150615_1833'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='matchdetail',
            unique_together=set([('match_id', 'region')]),
        ),
    ]
