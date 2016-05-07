from datetime import timedelta
import os

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"

CELERY_CREATE_MISSING_QUEUES = True

CELERY_DEFAULT_QUEUE = 'task_queue'

CELERY_ROUTES = {'starter_app.tasks.test_task': {'queue': 'test_queue'},}

# Redis
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')

CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_REDIS_MAX_CONNECTIONS = 1

# RabbitMQ
RABBIT_HOST = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', 'localhost')
RABBIT_PORT = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', '5672')

BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=os.environ.get('RABBITMQ_DEFAULT_USER', 'guest'),
    password=os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest'),
    hostname="%s:%s" % (RABBIT_HOST, RABBIT_PORT),
    vhost=os.environ.get('RABBITMQ_DEFAULT_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
# BROKER_HEARTBEAT = '?heartbeat=30'
# if not BROKER_URL.endswith(BROKER_HEARTBEAT):
#     BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10

# Celery settings
# Only add pickle to this list if your broker is secured from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = False
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

# BROKER_TRANSPORT = 'sqs'
# BROKER_TRANSPORT_OPTIONS = {
#     'region': 'eu-west-1',
#     'visibility_timeout': 30,
#     'polling_interval': 1,
# }
#

CELERYBEAT_SCHEDULE = {
    'periodic_test_task': {
        'task': 'starter_app.tasks.test_task',
        'schedule': timedelta(seconds=30),
        'args': ()
    },
    'periodic_default_task': {
        'task': 'starter_app.tasks.default_task',
        'schedule': timedelta(seconds=2),
        'args': ()
    }
}
