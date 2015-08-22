# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import app_one.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
            ],
        ),
        migrations.CreateModel(
            name='OneGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('group_name', models.CharField(max_length=200, null=True, blank=True)),
                ('group_icon', models.FileField(upload_to=app_one.models.get_group_icon_path, null=True, blank=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OneImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('image', models.FileField(upload_to=app_one.models.get_one_images_path, null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1, default='A')),
                ('group', models.ForeignKey(to='app_one.OneGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupimage',
            name='image',
            field=models.ForeignKey(to='app_one.OneImage'),
        ),
        migrations.AddField(
            model_name='groupimage',
            name='user_group',
            field=models.ForeignKey(to='app_one.UserGroup'),
        ),
    ]
