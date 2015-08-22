#!/bin/bash

unlink /etc/nginx/sites-enabled/nginx-uwsgi_one.conf
unlink /etc/uwsgi/vassals/uwsgi_one.ini

service nginx restart
