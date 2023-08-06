"""Flexenv, an environ-compatible tool for reading config as envvars"""


import yaml
import json
import os


class Environ:
    def __init__(self):
        self._env = {}

    def add_file(self, filename, optional=False):
        try:
            if filename.rfind('.yaml') >= 0:
                _parser = yaml
            elif filename.rfind('.json') >= 0:
                _parser = json
            else:
                raise NotImplementedError('File type not supported')
            with open(filename) as fp:
                self._env.update(_parser.load(fp))
        except Exception as e:
            if not optional:
                raise e

    def get(self, key, default=None):
        return self._env.get(key, os.environ.get(key, default))

    def set(self, key, value):
        self._env[key] = value

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)
