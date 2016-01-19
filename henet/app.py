# encoding: utf-8
import sys, os
from datetime import datetime
from socket import socket, SOCK_DGRAM, AF_INET
from functools import partial
import konfig

current_path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(current_path, os.path.pardir))

paths = [
    current_path,
    parent_path
]

for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

os.chdir(current_path)


#
# Import framework and controllers
#
import bottle
from beaker.middleware import SessionMiddleware

from bottle import route, run, view, app as app_stack
from bottle import TEMPLATE_PATH, request, static_file
from bottle import install


#
# Add view paths to the Bottle template path
#
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES_PATH)
RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources')
DEBUG = True
BIND_TO_PORT = 8080


@route("/resources/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root = RESOURCES_PATH)


@route("/heartbeat", method = "GET")
def heartbeat():
    return "A-OK ya'll!"


DEFAULT_CONFIG = os.path.join(parent_path, 'config.ini')


def main():
    print('running app')
    if len(sys.argv) > 1:
        config = konfig.Config(sys.argv[1])
    else:
        config = konfig.Config(DEFAULT_CONFIG)

    bottle.debug(DEBUG)

    app = bottle.app()
    cats = []
    for cat in config['henet']['categories']:
        values = dict(config[cat].items())
        cats.append((cat, values))

    app_stack.vars = app.vars = {'categories': cats}
    app_stack.view = partial(view, **app.vars)
    app_stack._config = app._config = config

    from henet import views
    #app = SessionMiddleware(bottle.app(), config.SESSION_OPTS)
    run(app=app, host="localhost", port=BIND_TO_PORT)


if __name__ == '__main__':
    main()
