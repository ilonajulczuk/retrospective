from fabric.colors import yellow
from utils import pjoin, config, cget
from fabric.operations import run
from fabric.contrib.files import upload_template


COMPONENT_NAME = 'Nginx congiguration files'

def started():
	upload_project_configuration()

def upload_project_configuration():
	source_file = pjoin(cget('deploy_files'), 'nginx',
						 'project.conf')
	target_file = pjoin(cget('services_dir'), 'nginx',
						'sites-available', cget('nginx_server_name'))

	# make sure that there is such directory
	run('mkdir -p {}'.format(pjoin(cget('services_dir'), 'nginx',
								   'sites-available')))
	run('mkdir -p {}'.format(pjoin(cget('project_dir'), 'logs')))
	
	print yellow('Uploading site configuration.')
	upload_template(source_file, target_file, config)

	print yellow('Testing configuration...')
	# test nginx congiguration
	# I wonder if using just sudo wouldn't be better here...
	run('sudo nginx -t')

def finished():
	print yellow('Restarting nginx')
	run('sudo /etc/init.d/nginx restart')