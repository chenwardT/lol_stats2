# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20160116_0301'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='championstats',
            unique_together=set([('bucket', 'champion_id')]),
        ),
    ]
