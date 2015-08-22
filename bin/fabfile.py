# from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager


# Hosts to deploy onto
def env_local():
    env.hosts = ['localhost']
    env.user = 'canary'
    # env.password = 'password'
    env.directory = '~/Projects/one-server/src/'
    # env.activate = '. ~/Projects/one-server/bin/activate'
    env.activate = 'workon one-server'


def env_staging():
    env.hosts = ['0.0.0.0']
    env.port = 22
    env.user = 'user'
    env.keyfile = '/home/user/.ssh/id_rsa_owtk.pem'
    env.password = ''
    env.directory = '/home/webapps/Projects/one-server/src/'
    # env.activate = 'source /home/webapps/Virtualenvs/one-server/bin/activate'
    env.activate = 'workon one-server'


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def test():
    with virtualenv():
        run('ls')


def migrate():
    with virtualenv():
        # local('./manage.py syncdb')
        local('./manage.py makemigrations app_name')
        local('./manage.py migrate app_name --database=default')


def prepare():
    with virtualenv():
        message = raw_input("Enter a git commit message:  ")
        local('git add . && git commit -a -m %s' % message)
        local('git push origin master')


def install():
    with virtualenv():
        run('pip install -r ../var/requirements/development.txt')
        run('sudo ../bin/install.sh')


def re_deploy():
    with virtualenv():
        run('git fetch --all')
        run('git reset --hard origin/master')
        run('./manage.py collectstatic -v0 --noinput')


def deploy():
    with virtualenv():
        # run('git commit -a -m "auto commit by fabfile"')
        run('git pull origin master')
        run('./manage.py collectstatic -v0 --noinput')
        run('touch ../etc/uwsgi/uwsgi_one.ini')
