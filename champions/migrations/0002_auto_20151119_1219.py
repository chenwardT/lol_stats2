# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='champion_id',
            field=models.IntegerField(serialize=False, primary_key=True, db_index=True),
        ),
    ]
