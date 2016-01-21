# encoding: utf-8
import sys
import os
from functools import partial

import bottle
from bottle import route, run, view, app as app_stack
from bottle import static_file
import konfig


HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)

RESOURCES_PATH = os.path.join(HERE, 'resources')
DEFAULT_DEBUG = True
DEFAULT_PORT = 8080
DEFAULT_HOST = 'localhost'
DEFAULT_CONFIG = os.path.join(HERE, '..', 'config.ini')


@route("/resources/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root=RESOURCES_PATH)


def main():
    if len(sys.argv) > 1:
        config = konfig.Config(sys.argv[1])
    else:
        config = konfig.Config(DEFAULT_CONFIG)

    bottle.debug(config['henet'].get('debug', DEFAULT_DEBUG))

    app = bottle.app()
    cats = []
    for cat in config['henet']['categories']:
        values = dict(config[cat].items())
        # defaults
        if not 'can_create' in values:
            values['can_create'] = True
        cats.append((cat, values))

    app_stack.vars = app.vars = {'categories': cats}
    app_stack.view = partial(view, **app.vars)
    app_stack._config = app._config = config

    from henet import views  # NOQA

    run(app=app,
        host=config['henet'].get('host', DEFAULT_HOST),
        port=config['henet'].get('port', DEFAULT_PORT))


if __name__ == '__main__':
    main()
