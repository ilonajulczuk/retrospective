from fabric.api import local, run, cd

from fabric.colors import yellow, red
from fabric.api import task, env
from fabric.decorators import hosts
from utils import configurable_task, virtualenv
from modules import pip


env.user = 'att'
env.hosts = ['rutherford.ro']
env.directory = '~/apps/retrospective/retrospective'


env.activate = 'source /home/att/apps/retrospective/bin/activate'
env.key_filename = '/home/att/.ssh/id_rsa'


@task
@hosts(u'att@rutherford.ro')
@configurable_task(default_config=u'config/devel.json')
def deploy_devel():
    deploy()


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

def wrap_critical(f):
    try:
        return f()
    except Exception as e:
        print red('Deploy aborted due to error:')
        print red(e.message, bold=True)
        return False

def deploy():
    code_dir = '~/apps/retrospective/'
    with cd(code_dir):
        run("git pull")
        with virtualenv():
            run('pip install -r requirements.txt')
            run("touch README.md")

    components = [pip]

    for component in components:
        print yellow('>> Starting "{}".'.format(component.COMPONENT_NAME),
                     bold=True)
        if not wrap_critical(component.started):
            return


    for component in reversed(components):
        print yellow('>> Starting "{}".'.format(component.COMPONENT_NAME),
                     bold=True)
        if not wrap_critical(component.finished):
            return