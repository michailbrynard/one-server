deploy:
	source activate one-server; \
		python ./src/manage.py collectstatic;
	rsync -rPh --exclude '.git' ../one-server amazon_one:/home/ubuntu/
