Usefull django stuff

You can use the following Postgres database credentials:
DB: django
User: django
Pass: oLOfESANSe

sudo su - postgres
createdb m4d_survey
createuser -P m4d_survey

psql
GRANT ALL PRIVILEGES ON DATABASE m4d_survey TO m4d_survey;
\q

./src/manage.py migrate --settings='config.settings.staging'

./src/manage.py loaddata src/survey/fixtures/sites.json --settings='config.settings.staging'
./src/manage.py loaddata src/survey/fixtures/group.json --settings='config.settings.staging'
./src/manage.py loaddata src/survey/fixtures/users.json --settings='config.settings.staging'

./src/manage.py sync --settings='config.settings.staging'
./src/manage.py reset_survey --settings='config.settings.staging'
./src/manage.py import_delegates --settings='config.settings.staging'


session = 'r0g8byzsvxlsulanhhmgmx7icqmifxx0'
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
session = Session.objects.get(session_key=session)
uid = session.get_decoded().get('_auth_user_id')
user = User.objects.get(pk=uid)
