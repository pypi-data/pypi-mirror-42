# -*- coding: utf-8 -*
# System imports
from urlparse import urlparse

# Third-party imports
from tc_core.web import RequestParser
import tornado
from thumbor.handlers.imaging import ImagingHandler
# Local imports


class UrlAliasesHandler(ImagingHandler):

    @classmethod
    def regex(cls):
        return r'/a/(?P<alias>[^\/]+)/?(?P<img_url>.+)?'

    @tornado.gen.coroutine
    def get(self, **kwargs):
        alias = kwargs['alias']
        img_url = kwargs['img_url']
        long_url = self.storage.get(alias)
        if not all([alias, img_url, long_url]):
            raise tornado.web.HTTPError(404)

        url = '{}/{}'.format(long_url, img_url)
        self.request.uri = urlparse(url).path
        options = RequestParser.path_to_parameters(self.request.uri)
        super(UrlAliasesHandler, self).get(**options)

    @property
    def storage(self):
        if hasattr(self, '_storage'):
            return self._storage
        self._storage = self.context.modules.aliases_storage
        return self._storage
