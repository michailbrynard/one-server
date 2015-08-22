# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_auto_20150814_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbasic',
            name='email',
            field=models.EmailField(blank=True, error_messages={'required': 'Email field is required.'}, verbose_name='email address', max_length=254, unique=True),
        ),
    ]
