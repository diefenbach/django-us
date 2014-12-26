# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('us', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 26, 14, 7, 0, 34243, tzinfo=utc), verbose_name='Created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='url',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 26, 14, 7, 15, 615885, tzinfo=utc), verbose_name='Modified', auto_now=True),
            preserve_default=False,
        ),
    ]
