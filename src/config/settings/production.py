from config.settings.common import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'config.wsgi.application'
# BASE_URL = 'http://127.0.0.1/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chappie',
        'USER': 'chappie',
        'PASSWORD': 'a0-=mwd_=l&r=wky6rf-zh##y@ayzp0a)rm(@)hz!keisd5c-&',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# EMAIL
# ---------------------------------------------------------------------------------------------------------------------
# For possible shortcuts see django.core.mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'user@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'

DEFAULT_FROM_EMAIL = 'webmaster@localhost'
SERVER_EMAIL = 'Mail Admin Error messages <error@gmail.com>'  #