#!/bin/bash

# Change password here:
PASSWORD=wVi2iEJDX

backup_date=`date +"%y-%m-%d_%H-%M"`
project_dir=/home/webapps/Projects/one/
uid=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
file_name=backup_${uid}.${backup_date}.zip

zip --password ${PASSWORD} \
    -r ${project_dir}/var/www/media/backups/${file_name} ${project_dir} \
    -x *.git* \
    -x *.sock -x *__pycache__* -x *var/www/static* -x *.svg -x *.log -x *.zip


cp ${project_dir}/var/www/media/backups/${file_name} /home/ensync/backups/

link="http:///media/backups/${file_name}"

echo -e '\n'
echo "Link to zip download:"
echo ${link}
echo -e '\n'
echo "SCP command:"
echo "scp @:/home/webapps/backups/${file_name} backup.zip"
