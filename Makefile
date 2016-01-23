deploy:
	source activate one-server; \
		python ./src/manage.py collectstatic --noinput;
	rsync -rPh --exclude '.git' --exclude '__pycache__' ../one-server amazon_one:/home/ubuntu/

sync_data:
	scp amazon_one:/home/ubuntu/one-server/src/django.db ./src/django.db
	rsync -rPh amazon_one:/home/ubuntu/one-server/var/www/media/ ./var/www/media/

reset_db:
	rm -rf ./src/django.db
	rm -rf ./src/administration/migrations/
	rm -rf ./src/app_one/migrations/
	source activate one-server; \
    		python ./src/manage.py makemigrations administration app_one; \
    		python ./src/manage.py migrate; \
    		python ./src/manage.py createsuperuser --email=admin@zapgo.co --username=admin; \
    		python ./src/manage.py loaddata user_data.json friends_data.json images_data.json snortie_data.json; \

reload_server:
	ssh amazon_one "cd one-server; docker-compose restart;"
