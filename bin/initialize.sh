#!/bin/sh
chmod -R ug+x bin/
chmod ug+x src/manage.py

read -p "Install bower? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    cd var/www/static/app/
    bower install
    cd /home/webapps/Projects/one
fi

read -p "Initialize Git? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    mv example.gitignore .gitignore
    git init
    git add .
    git commit -a -m "Initial commit!"
fi

read -p "Create Git remote? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    ssh -t ocean_ssh "sudo /srv/data/git/git-shell-commands/create one"
    
    git remote add origin ssh://ocean_git/~/one
    git push --set-upstream origin master
fi

read -p "Register subdomain? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # TODO: Namecheap API for for obitec.ga
    echo "Not yet implemented, go to freenom.com or namecheap.com and register domain/subdomain"
    echo "Remember to update the nginx config file to correct domain"
fi
