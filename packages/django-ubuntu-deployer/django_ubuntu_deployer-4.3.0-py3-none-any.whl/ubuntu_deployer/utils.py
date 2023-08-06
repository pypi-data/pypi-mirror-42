import os

import ubuntu_deployer


def get_gunicorn_config():
    with open(os.path.join(os.path.dirname(ubuntu_deployer.__file__), 'configs', 'gunicorn_config.txt'), 'r') as f:
        return f.read()


def get_nginx_config():
    with open(os.path.join(os.path.dirname(ubuntu_deployer.__file__), 'configs', 'nginx_config.txt'), 'r') as f:
        return f.read()


def paths_exists(*args):
    if not args:
        raise ValueError('Not set arg or args.')
    for arg in args:
        if not os.path.exists(arg):
            return False
    return True
