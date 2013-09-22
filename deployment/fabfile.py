from fabric.api import local, run, cd

from fabric.colors import yellow, green
from fabric.api import task, env
from fabric.decorators import hosts
from utils import configurable_task, wrap_critical
from modules import pip, git, nginx, gunicorn, django


env.user = 'att'
env.key_filename = '/home/att/.ssh/id_rsa'


@task
def prepare_deploy():
    test()
    commit()
    push()

def test():
    local("../manage.py test core")


def commit():
    local("git add -p && git commit")


def push():
    local("git push")


@task
@hosts('att@rutherford.ro')
def init_devel_deployment():
    init_deployment('retrospective_devel')


@task
@hosts('att@rutherford.ro')
def init_stable_deployment():
    init_deployment('retrospective_stable')


def init_deployment(app_name):
    with cd('~/apps'):
        run('mkdir -p {}'.format(app_name))

    code_dir = '~/apps/{}/'.format(app_name)
    with cd(code_dir):
        print yellow("Cloning from remote repository", bold=True)
        run('git clone git@github.com:atteroTheGreatest/retrospective.git code')
        print yellow("Initialising virtualenv", bold=True)
        run('virtualenv .')
        print green('Success!', bold=True)


@task
@hosts(u'att@rutherford.ro')
@configurable_task(default_config=u'config/devel.json')
def deploy_devel():
    deploy()


def deploy():

    components = [git, pip, django, gunicorn, nginx]

    for component in components:
        print yellow('>> Starting "{}".'.format(component.COMPONENT_NAME),
                     bold=True)
        if not wrap_critical(component.started):
            return


    for component in reversed(components):
        print yellow('>> Finishing "{}".'.format(component.COMPONENT_NAME),
                     bold=True)
        if not wrap_critical(component.finished):
            return

    print green("Success! Deployment done.", bold=True)