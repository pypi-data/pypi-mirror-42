# -*- coding: utf-8 -*-
# System imports
# Third-party imports
from derpconf.config import Config
from tc_core import Extension, Extensions

# Local imports
from thumbor_aliases.handlers.aliases import UrlAliasesHandler


extension = Extension('thumbor_aliases')

# Register modules for settings
extension.add_module(
    config_key='ALIASES_STORAGE',
    class_name='AliasesStorage',
    multiple=False
)

# Register main handler
extension.add_handler(UrlAliasesHandler.regex(), UrlAliasesHandler)

# Define settings
Config.define('ALIASES_STORAGE', 'thumbor_aliases.storages.yml_file',
              'Aliases storage class', 'URL Aliases')
Config.define('ALIASES_STORAGE_FILE', '~/aliases.yml', 'Aliases file name')

Extensions.register(extension)
