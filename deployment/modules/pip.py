from utils import virtualenv, cget, pjoin
from fabric.colors import yellow
from fabric.operations import run


COMPONENT_NAME = 'Pip requirements'


def started():
	req_dir = pjoin(cget('code_dir'), 'deployment', 'files', 'requirements')
	with virtualenv():
			for requirement in cget('pip_requirements', []):
				print yellow("Installing {}".format(requirement))
				run('pip install -r {}'.format(pjoin(req_dir, requirement)))


def finished():
	pass