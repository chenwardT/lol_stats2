# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20160116_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='is_exact_version',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
