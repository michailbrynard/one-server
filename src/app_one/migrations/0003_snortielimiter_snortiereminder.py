# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_one', '0002_auto_20150912_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnortieLimiter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('message', models.TextField(null=True, blank=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], default='A', max_length=1)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SnortieReminder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('message', models.TextField(null=True, blank=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], default='A', max_length=1)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
