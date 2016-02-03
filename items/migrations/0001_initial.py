# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.IntegerField(serialize=False, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('plaintext', models.TextField(blank=True)),
                ('group', models.CharField(blank=True, max_length=36)),
                ('name', models.CharField(max_length=42)),
            ],
        ),
    ]
