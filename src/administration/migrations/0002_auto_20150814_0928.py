# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbasic',
            name='gender',
            field=models.CharField(max_length=15, default='Male', choices=[('Female', 'Female'), ('Male', 'Male')]),
        ),
    ]
