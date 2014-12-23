# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(verbose_name='Url')),
                ('short_url', models.CharField(unique=True, max_length=50, verbose_name='Short URL')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
