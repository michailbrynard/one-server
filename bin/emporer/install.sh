#!/bin/bash

#sudo pip3 install uwsgi
sudo apt-get install uwsgi

sudo mkdir -p /etc/uwsgi/vassals/
sudo chown -R webapps:webapps /etc/uwsgi/vassals

sudo touch /etc/uwsgi/emporer.ini
sudo chown webapps:webapps /etc/uwsgi/emperor.ini

cat <<EOT >> /etc/uwsgi/emperor.ini
[uwsgi]
emperor         = /etc/uwsgi/vassals
master          = true
uid             = webapps
gid             = webapps
daemonize       = /var/log/emporer.log
pidfile         = /tmp/emporer.pid
vacuum          = true
EOT

./bin/emporer/reload.sh