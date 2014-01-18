from fabric.api import run, env
from fabric.context_managers import cd
import os

env.hosts = ['root@0.0.0.0:1337']


def update_podcasts():
    with cd('"{}"'.format(os.path.dirname(__file__))):
        run('python3 manage.py updatepodcasts')


def setup_dev():
    with cd('"{}"'.format(os.path.dirname(__file__))):
        run('python3 manage.py syncdb')
        run('python3 manage.py loaddata sample_podcasts')
        update_podcasts()
        run('python3 manage.py fetchepisodes')
