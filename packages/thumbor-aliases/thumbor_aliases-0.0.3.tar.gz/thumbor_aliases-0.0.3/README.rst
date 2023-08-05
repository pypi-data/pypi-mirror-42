
Thumbor URL Aliases plugin
==========================
.. image:: https://travis-ci.org/bluekiri/thumbor-aliases.svg?branch=master
**thumbor_aliases** let's you create custom urls to redirect your most-used request
using a friendly url.

Imagine that your company decides that all thumbnails should go to ``100x100/smart``.

Wouldn't be awesome to just name this url: ``thumbnail``? So, if you need to change
it later, you can even just modify the alias to point to ``200x200/smart`` instead,
without having to change your application code.


Install
^^^^^^^^^^
Before installing, be sure you're using Python2.7 (Python3 isn't supported yet).

Install it by using pip::

  $  pip install thumbor-aliases
 
Easy, right?

Configure
^^^^^^^^^
Create, if not done yet, your thumbor config file::

  $ thumbor-config > config.cfg
  
And enable **thumbor_aliases** plugin on community extensions. This can be done by
just adding next lines at the end of configuration file::

  COMMUNITY_EXTENSIONS = [
    'thumbor_aliases',
    ...
  ]

By default it will use the ``yaml_file`` storage handler, which reads a file located on ``~/aliases.yml``.

In case you want to change the file location, you can set the config variable: ``ALIASES_STORAGE_FILE`` ::

  ALIASES_STORAGE_FILE = "~/your_custom_filename.yml"
  
The YAML file should follow next format::

  alias: "url/to/redirect"
  
For example::

  thumbnail: "100x100/smart"
  header: "800x200/smart"
  
And in order to finally execute the app and let the magic happen, run next command::

  $ thumbor --conf=your_thumbor_config.cfg -a tc_core.app.App
