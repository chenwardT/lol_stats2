# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='lane',
            field=models.CharField(max_length=16, default='UNSET'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bucket',
            name='role',
            field=models.CharField(max_length=16),
        ),
    ]
