# -*- coding: utf-8 -*-
# System imports
# Third-party imports
# Local imports


class BaseStorage(object):
    def __init__(self, context):
        self.context = context
        self.prepare()

    def prepare(self):
        pass

    @property
    def config(self):
        return self.context.config

    def get(self, alias):
        raise NotImplementedError('To implement on child class')

    def put(self, alias, long_url):
        raise NotImplementedError('Put is not implemented for this storage')

    def delete(self, alias):
        raise NotImplementedError('Delete is not implemented for this storage')
