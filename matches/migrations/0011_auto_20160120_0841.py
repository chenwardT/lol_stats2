# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0010_auto_20151118_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchdetail',
            name='queue_type',
            field=models.CharField(max_length=32),
        ),
    ]
