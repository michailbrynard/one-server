import os
import multiprocessing

PROJECT_NAME = 'one-server'
PROJ_DIR = os.path.join('/home/webapps/Projects/', PROJECT_NAME)
proc_name = PROJECT_NAME
# user = PROJECT_NAME
# group = 'webapps'
workers = multiprocessing.cpu_count() * 2 + 1
log_level = 'info'
# bind = 'unix:%s' % os.path.join(PROJ_DIR, 'tmp/gunicorn.sock')
timeout = 300
max_requests = 50
daemon = True
# pidfile = os.path.join(PROJ_DIR, 'tmp/gunicorn.pid')
# umask = 7
# tmp_upload_dir = os.path.join(PROJ_DIR, 'tmp/')
# worker_tmp_dir = os.path.join(PROJ_DIR, 'tmp/')
# raw_env = ['TMPDIR=%s' % os.path.join(PROJ_DIR, 'run/tmp/')]#,'DJANGO_SETTINGS_MODULE=config.settings.production']

