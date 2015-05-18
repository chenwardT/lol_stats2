# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('champion_id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('key', models.CharField(max_length=32)),
            ],
        ),
    ]
