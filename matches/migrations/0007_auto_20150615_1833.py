# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_auto_20150612_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participanttimeline',
            name='participant',
            field=models.ForeignKey(to='matches.Participant'),
        ),
    ]
