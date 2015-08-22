DJSKEL - Django Project template
================================

DjSkel is a heavyweight project template for Django. The folder structure is set up to mimic UNIX folder structure. The django source directory is src.

How to use
----------
1. Download and install [Anaconda](https://warehouse.python.org/project/gunicorn/) for Python 3.4
2. Create virtual python environment
    ```bash
    export PATH=~/anaconda3/bin/:$PATH
    conda update conda
    conda create -n webdev python=3.4 pip django
    source activate webdev
    ```

3. Create django project from template
    ```bash
       django-admin startproject --template=https://github.com/obitec/djskel/archive/master.zip --extension=py --extension=conf --extension=sh --extension=ini --extension=rst {{ project_name }}
    ```
4. Run the installer
```bash
./bin/initialize.sh 
```


How to deploy
-------------
1. Run the installer
    ```bash
    ./bin/setup/ubuntu.sh
    ```




Feutures
--------
- conda env create
- Django 1.7 or newer (TODO 1.8 and above)
- UWSGI
- Gunicorn
- Nginx
- Postgresql
- Fig (TODO update for docker-compose)
- Docker
- Vagrant
- Celery (TODO)
- Redis (TODO)
- Custom User model (TODO)
- Munin
- Jinja2 templating by default (TODO)
- Yeoman webapp integration (TODO)
- requirejs

Django Extensions
-----------------
- Grappelli
- Rest Framework 3
- Guardian
- Report Builder

Custom Apps
--------------
- FactBook
- Issue Tracker
- Munin


