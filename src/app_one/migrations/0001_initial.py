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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='A', max_length=1, choices=[('A', 'Active'), ('D', 'Disabled')])),
            ],
            options={
                'ordering': ('-created_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='ImageMany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=app_one.models.get_one_images_path)),
                ('description', models.CharField(blank=True, null=True, max_length=200)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OneGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('group_name', models.CharField(blank=True, null=True, max_length=200)),
                ('group_icon', models.ImageField(blank=True, null=True, upload_to=app_one.models.get_group_icon_path)),
                ('status', models.CharField(default='A', max_length=1, choices=[('A', 'Active'), ('D', 'Disabled')])),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
        ),
        migrations.CreateModel(
            name='OneImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=app_one.models.get_one_images_path)),
                ('description', models.CharField(blank=True, null=True, max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='A', max_length=1, choices=[('A', 'Active'), ('D', 'Disabled')])),
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
