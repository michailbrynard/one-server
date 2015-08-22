#!/bin/sh
mkdir -p var/log
mkdir -p var/www/media/uploads
mkdir -p tmp

touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginx-access.log

chmod -R ug+x bin/
chmod ug+x src/manage.py