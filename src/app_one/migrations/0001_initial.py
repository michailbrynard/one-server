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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(null=True, upload_to=app_one.models.get_one_images_path, blank=True)),
                ('description', models.CharField(null=True, blank=True, max_length=200)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='OneGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(null=True, blank=True, max_length=200)),
                ('group_icon', models.FileField(null=True, upload_to=app_one.models.get_group_icon_path, blank=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], default='A', max_length=1)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Disabled')], default='A', max_length=1)),
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