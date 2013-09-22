from fabric.api import local, run, cd
from fabric.api import *
from contextlib import contextmanager as _contextmanager


env.user = 'att'
env.hosts = ['rutherford.ro']
env.directory = '~/apps/retrospective/retrospective'

def hello():
   print("Hello world!")


env.activate = 'source /home/att/apps/retrospective/bin/activate'
env.key_filename = '/home/att/.ssh/id_rsa'
@_contextmanager
def virtualenv():
    with prefix(env.activate):
        yield

def test():
    local("../manage.py test retrospective")


def commit():
    local("git add -p && git commit")


def push():
    local("git push")


def prepare_deploy():
    test()
    commit()
    push()
    

def init_deployment():
    code_dir = '~/apps/'
    with cd(code_dir):
        run('git clone git@github.com:atteroTheGreatest/retrospective.git')
        run('virtualenv retrospective')


def deploy():
    code_dir = '~/apps/retrospective/'
    with cd(code_dir):
        run("git pull")
        with virtualenv():
            run('pip install -r requirements.txt')
            run("touch README.md")

