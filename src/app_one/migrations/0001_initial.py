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
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=app_one.models.get_one_images_path)),
                ('description', models.CharField(blank=True, null=True, max_length=200)),
                ('created_timestamp', models.DateTimeField(null=True, auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SnortieLimiter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='A', choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SnortieReminder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='A', choices=[('A', 'Active'), ('D', 'Disabled')], max_length=1)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriend',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('invite_reference', models.CharField(blank=True, null=True, max_length=200)),
                ('friend_status', models.CharField(default='Invited',
                                                   choices=[('Invited', 'Invited'), ('Pending', 'Pending'),
                                                            ('Friends', 'Friends'), ('Declined', 'Declined'),
                                                            ('Removed', 'Removed'), ('NotOnOneYet', 'NotOnOneYet')],
                                                   max_length=15)),
                ('invited_timestamp', models.DateTimeField(auto_now_add=True)),
                ('accepted_timestamp', models.DateTimeField(blank=True, null=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                (
                'friend', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='friend')),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
