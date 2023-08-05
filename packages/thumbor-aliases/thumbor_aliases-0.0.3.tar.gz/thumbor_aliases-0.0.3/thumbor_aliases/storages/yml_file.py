# -*- coding: utf-8 -*-
# System imports
import os

# Third-party imports
import yaml

# Local imports
from .base import BaseStorage


class AliasesStorage(BaseStorage):

    @staticmethod
    def _read_from_file(filename):
        with open(filename, 'r') as fopen:
            _config = yaml.load(fopen)
        return _config

    def prepare(self):
        aliases_file = os.path.expanduser(
            self.config.get('ALIASES_STORAGE_FILE')
        )
        if not aliases_file:
            raise Exception('No well configured')
        self._aliases_dict = self._read_from_file(aliases_file)

    def get(self, alias):
        """ Return the url for an alias """
        return self._aliases_dict.get(alias)
