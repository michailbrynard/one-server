#!/bin/bash


# CREATE USER AND GROUPS
# --------------------------------------------------------------------------------------------------------------------#
sudo mkdir -p /home/webapps/projects
sudo addgroup webapps --system
sudo adduser --system --ingroup webapps --home /home/webapps webapps
sudo adduser canary webapps
sudo adduser www-data webapps
sudo chown -R webapps:webapps /home/webapps/
sudo chmod -R +s /home/webapps/
sudo chmod -R g+w /home/webapps/


# SSH SETUP
# --------------------------------------------------------------------------------------------------------------------#
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa -b 4096
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
eval `ssh-agent -s`
ssh-add .ssh/id_rsa
vi ~/.ssh/id_rsa # copy this to computer
vi ~/.ssh/id_rsa_git # paste this here
chmod 600 ~/.ssh/id_rsa_git
cat <<EOT >> .ssh/config
Host ocean_git
    HostName 196.28.18.116
    Port 8622
    User git
    IdentityFile ~/.ssh/id_rsa_git
EOT

sudo vi /etc/ssh/sshd_config # update values here
sudo service ssh restart


# INSTALL DEPENDENIES
# --------------------------------------------------------------------------------------------------------------------#
sudo apt-get install ncurses-term htop vim python3-pip nginx git npm postgresql
sudo npm install -g bower
sudo pip3 install uwsgi

# TODO: Build and install lates vim and bash from source


# CONFIGURE ENVIRONMENT
# --------------------------------------------------------------------------------------------------------------------#
git clone git://github.com/andsens/homeshick.git $HOME/.homesick/repos/homeshick
printf '\nsource "$HOME/.homesick/repos/homeshick/homeshick.sh"' >> $HOME/.bashrc
source .bashrc
source .bash_profile
homeshick clone ssh://ocean_git/~/castle


# CONFIGURE UWSGI
# --------------------------------------------------------------------------------------------------------------------#
sudo mkdir -p /etc/uwsgi/vassals
cat <<EOT >> /home/webapps/emporer.ini
uwsgi -c /home/webapps/emporer.ini
EOT


# INSTALL AND CONFIDURE MINICONDA
# --------------------------------------------------------------------------------------------------------------------#
wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
chmod +x miniconda.sh

export PATH=/home/canary/miniconda/bin:$PATH
conda update --yes conda 
conda create --yes -n webapps python=3.4 ipython django pip

#git clone ssh://ocean_git/~/djskel /home/webapps/projects/djskel

# TODO: Create a workon script
#vi workon.sh
#export PATH=/home/canary/miniconda/bin/:$PATH && source activate webapps
#source activate webapps
#chmod +x workon.sh
#source ./workon.sh

sudo chown canary:canary /home/canary/.config/


# CLEANUP
# --------------------------------------------------------------------------------------------------------------------#
sudo passwd -l root

history -c
history -w