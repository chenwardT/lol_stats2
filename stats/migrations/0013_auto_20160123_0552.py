# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0003_significantposition'),
        ('stats', '0012_auto_20160123_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='championstats',
            name='champion',
            field=models.ForeignKey(default=212, to='champions.Champion'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='championstats',
            unique_together=set([('bucket', 'champion')]),
        ),
    ]
