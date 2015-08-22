#!/bin/bash


# User and Security
# --------------------------------------------------------------------------------------------------------------------#
adduser --disabled-password --gecos "" $USERNAME
adduser $USERNAME sudo
usermod --password $(echo $PASSWORD | openssl passwd -1 -stdin) $USERNAME

usermod -aG docker canary

su - $USERNAME

# SSH
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -q -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa

cat ~/.ssh/id_rsa.pub >> .ssh/authorized_keys

eval `ssh-agent -s`
ssh-add ~/.ssh/id_rsa

# sudo vi /etc/ssh/sshd_config # update values here

sed -i 's/^#?Port .*/Port 2222/' /etc/ssh/sshd_config
sed -i 's/^#?PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/^#?PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config

sudo service ssh restart
cat .ssh/id_rsa
# copy and save to computer
# add details to ssh/config
# use config to log in to new server

cat <<EOT >> .ssh/config
Host ocean_git
    HostName 196.28.18.116
    Port 8622
    User git
    IdentityFile ~/.ssh/id_rsa_git
EOT

vi ~/.ssh/id_rsa_git # paste this here
chmod 600 ~/.ssh/id_rsa_git

# Kill root
sudo passwd -l root


# INSTALL DEPENDENIES
# --------------------------------------------------------------------------------------------------------------------#
sudo perl -pi.bak -e 's/archive\.ubuntu\.com\/ubuntu/ubuntu\.saix\.net\/ubuntu-archive\//g' /etc/apt/sources.list
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim tree htop ncurses-term git 
sudo apt-get install ncurses-term htop vim-nox vim python3-pip nginx git postgresql munin awstats npm
sudo npm install -g bower
sudo pip3 install uwsgi

# LOCALE
dpkg-reconfigure locales tzdata # check syntax


# CONFIGURE ENVIRONMENT
# --------------------------------------------------------------------------------------------------------------------#
git clone git://github.com/andsens/homeshick.git $HOME/.homesick/repos/homeshick
printf '\nsource "$HOME/.homesick/repos/homeshick/homeshick.sh"' >> $HOME/.bashrc
source .bashrc
source .bash_profile
homeshick clone ssh://ocean_git/~/castle


# INSTALL AND CONFIDURE MINICONDA
# --------------------------------------------------------------------------------------------------------------------#
# INSTALL AND CONFIDURE MINICONDA
# --------------------------------------------------------------------------------------------------------------------#
wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b

export PATH=/home/canary/miniconda/bin:$PATH
conda update --yes conda 
conda create --yes -n webapps python=3.4 ipython django pip


# DJANGO VIRTUALENV + USERS
addgroup webapps --system
adduser --system --ingroup webapps --home /home/webapps webapps

adduser canary webapps

chown -R webapps:webapps /home/webapps/

chmod -R +s /home/webapps/
chmod -R g+w /home/webapps/

mkdir -p /home/webapps/Projects
mkdir -p /home/webapps/Virtualenvs

adduser www-data webapps


# SERVERS
sudo pip3 install uwsgi
sudo mkdir -p /etc/uwsgi/vassals


history -c
history -w



# DOCKER
# --------------------------------------------------------------------------------------------------------------------#
#sudo apt-get install docker

sudo -i
wget -qO- https://get.docker.com/ | sh
curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
usermod -aG docker canary

# NGINX SSL
# --------------------------------------------------------------------------------------------------------------------#
#sudo apt-get install docker
















