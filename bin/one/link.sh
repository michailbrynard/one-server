#!/bin/bash
sudo chown -R canary:webapps /home/webapps/Projects/one
sudo chmod -R g+w /home/webapps/Projects/one

ln -s /home/webapps/Projects/one/etc/uwsgi/nginx-uwsgi_one.conf /etc/nginx/sites-enabled/
ln -s /home/webapps/Projects/one/etc/uwsgi/uwsgi_one.ini /etc/uwsgi/vassals/

sudo service nginx restart