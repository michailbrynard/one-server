# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oneimage',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='oneimage',
            name='updated_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
