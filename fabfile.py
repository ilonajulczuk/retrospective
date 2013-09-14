from fabric.api import local, settings, abort, run, cd
from fabric.api import *
from fabric.contrib.console import confirm


env.user = 'ubuntu'
env.hosts = ['ec2-54-213-160-123.us-west-2.compute.amazonaws.com']
env.key_filename = '~/keys/attero.pem'

def hello():
   print("Hello world!")


def prepare_deploy():
    local("git add -p && git commit")
    local("git push")


def deploy():
    env.user = 'ubuntu'
    env.hosts = ['ec2-54-213-160-123.us-west-2.compute.amazonaws.com']
    code_dir = '~/apps/retrospective/retrospective'
    with cd(code_dir):
        run("git pull")
        run("touch readme.md")
