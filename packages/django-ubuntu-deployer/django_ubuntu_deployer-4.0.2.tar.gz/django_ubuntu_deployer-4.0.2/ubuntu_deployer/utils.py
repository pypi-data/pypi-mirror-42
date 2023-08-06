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


class DeployOptions(dict):
    def __init__(self, *args, **kwargs):
        extras = kwargs.pop('extras', {})
        super(DeployOptions, self).__init__(*args, **kwargs)
        if isinstance(extras, (list, tuple)):
            extras = {key: value for extra in extras if isinstance(extra, dict) for key, value in extra.items()}
        for key, value in self.items():
            if isinstance(value, str):
                self[key] = value.format(**extras, **self._self_prefix())

    def _self_prefix(self):
        return {'self_{}'.format(key): value for key, value in self.items()}
