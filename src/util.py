import os


def get_config_from_syspath(name):
    for path in os.getenv('PYTHONPATH').split(os.pathsep):
        if os.path.exists(os.path.join(path, name)):
            return os.path.join(path, name)
        return name
