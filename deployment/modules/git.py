from fabric.context_managers import cd
from fabric.operations import run
from utils import cget, pjoin

COMPONENT_NAME = 'Git code repository'


def started():
	code_dir = pjoin(cget('project_dir'), 'code')
	with cd(code_dir):
		code_branch = cget('branch', 'master')
		run('git clean -f')
		run('git fetch origin')
		run('git reset --hard origin/{}'.format(code_branch))


def finished():
	pass