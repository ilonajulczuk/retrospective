from utils import virtualenv, cget
from fabric.colors import yellow
from fabric.api import run, cd


COMPONENT_NAME = "Django project, db syncing"


def started():
    sync_database()


def sync_database():
    with virtualenv():
        with cd(cget(u'code_dir')):
            print yellow('Migrating database')
            run('python manage.py syncdb --migrate')


def finished():
    pass
