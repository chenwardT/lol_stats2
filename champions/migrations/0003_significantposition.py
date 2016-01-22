# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0002_auto_20151119_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignificantPosition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('version', models.CharField(max_length=16)),
                ('lane', models.CharField(max_length=16)),
                ('role', models.CharField(max_length=16)),
                ('pct', models.FloatField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('champion', models.ForeignKey(to='champions.Champion')),
            ],
        ),
    ]
