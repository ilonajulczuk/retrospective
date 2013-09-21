from fabric.api import local, run, cd
from fabric.api import *


def hello():
   print("Hello world!")


def prepare_deploy():
    local("git add -p && git commit")
    local("git push")


def deploy():
    env.user = 'att'
    env.hosts = ['rutherford.ro']
    code_dir = '~/apps/retrospective/retrospective'
    with cd(code_dir):
        run("git pull")
        run("touch README.md")
