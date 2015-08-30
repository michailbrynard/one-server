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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=1, default='A', choices=[('A', 'Active'), ('D', 'Disabled')])),
            ],
            options={
                'ordering': ('-created_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='ImageMany',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=app_one.models.get_one_images_path, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OneGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=200, null=True)),
                ('group_icon', models.ImageField(blank=True, upload_to=app_one.models.get_group_icon_path, null=True)),
                ('status', models.CharField(max_length=1, default='A', choices=[('A', 'Active'), ('D', 'Disabled')])),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OneImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=app_one.models.get_one_images_path, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=1, default='A', choices=[('A', 'Active'), ('D', 'Disabled')])),
                ('group', models.ForeignKey(to='app_one.OneGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='imagemany',
            name='groups',
            field=models.ManyToManyField(to='app_one.OneGroup'),
        ),
        migrations.AddField(
            model_name='imagemany',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
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
