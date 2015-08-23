deploy:
	source activate one-server; \
		python ./src/manage.py collectstatic --noinput;
	rsync -rPh --exclude '.git' --exclude '__pycache__' ../one-server amazon_one:/home/ubuntu/

sync_data:
	scp amazon_one:/home/ubuntu/one-server/src/django.db ./src/django.db
	rsync -rPh amazon_one:/home/ubuntu/one-server/var/www/media/ ./var/www/media/


