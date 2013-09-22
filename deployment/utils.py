from fabric.operations import run
from fabric.api import env, prefix
from functools import wraps, partial
from contextlib import contextmanager
import json
import operator
import os


DEFAULT_CONFIG_FILENAME = 'config/defaults.json'

config = {}
pjoin = os.path.join
pdir = os.path.dirname
cget = config.get
cset = partial(operator.setitem, config)


def configurable_task(default_config=None):
    """Task which can be given path to custom config

    Usage: use decorator on task and pass filename to config
    in brackets
    """
    def wrapper(f):
        @wraps(f)
        def inner(config_filename=default_config, *args, **kwargs):
            load_config(config_filename)
            return f(*args, **kwargs)
        return inner
    return wrapper


def load_config(config_filename):
    with open(DEFAULT_CONFIG_FILENAME, 'rb') as f:
        config.update(json.load(f))

    if config_filename is not None:
        init_custom_config(config_filename)


def init_custom_config(config_filename):
    with open(config_filename, 'rb') as f:
        config.update(json.load(f))

    remote_home = run('echo "${HOME}"')
    update_paths(remote_home)


def update_paths(remote_home):
    project_dir = pjoin(remote_home, cget('project_name'))
    cset('project_dir', project_dir)
    modules_names = ['code', 'venv', 'logs', 'services']
    suffix = '_dir'
    for name in modules_names:
        cset(name + suffix, pjoin(project_dir, name))

    files_dir = pjoin(pdir(env['real_fabfile']), 'files')
    cset('deploy_files', files_dir)


@contextmanager
def virtualenv():
    with prefix(env.activate):
        yield