"""
An enhanced version of pelican-livereload.py from [1] and [2].

Reference
---------
[1] Using LiveReload with Pelican
    https://merlijn.vandeen.nl/2015/pelican-livereload.html
[2] LiveReload with Pelican
    http://tech.agilitynerd.com/livereload-with-pelican.html


This script accepts some arguments to configure Pelican's article generation.

+ content: Path to content directory. This path is joined to `PATH` value in
    Pelican's settings dictionary.
+ host and port: Host name and Port number are variable.
+ open_url: If True, a default browser will open.
+ relative: If True, relative URLs are used which are useful when testing
    locally. Thanks to this option, you don't need to change `RELATIVE_URLS`
    of `pelicanconf.py` in developing mode. You can always set `RELATIVE_URLS`
    to False.
"""

from functools import partial

from livereload import Server
from pelican import Pelican
from pelican.settings import read_settings


def build(pelican):
    try:
        pelican.run()
    except SystemExit:
        pass


def serve(host: str, port: int, open_url: bool = False,
          relative: bool = True) -> None:
    settings = read_settings('pelicanconf.py')
    settings['RELATIVE_URLS'] = relative
    pelican = Pelican(settings)

    _build = partial(build, pelican)
    _build()

    server = Server()
    server.watch(pelican.settings['PATH'], _build)
    server.watch(pelican.settings['THEME'], _build)
    server.watch('./pelicanconf.py', _build)

    server.serve(port=port, host=host, root=settings['OUTPUT_PATH'],
                 open_url_delay=open_url)
