echo "Initilizing {{ project_name }}"

if not exist var\log mkdir var\log
if not exist var\www\media\uploads mkdir var\www\media\uploads
if not exist tmp mkdir tmp

type NUL > var\log\django.log

