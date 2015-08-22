# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_one.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.FileField(upload_to=app_one.models.get_one_images_path, blank=True, null=True)),
                ('description', models.CharField(max_length=200, blank=True, null=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
            ],
        ),
        migrations.CreateModel(
            name='OneGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('group_name', models.CharField(max_length=200, blank=True, null=True)),
                ('group_icon', models.FileField(upload_to=app_one.models.get_group_icon_path, blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
                ('group', models.ForeignKey(to='app_one.OneGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupimage',
            name='user_group',
            field=models.ForeignKey(to='app_one.UserGroup'),
        ),
    ]
