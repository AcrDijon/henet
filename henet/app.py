# encoding: utf-8
import sys, os
from datetime import datetime
from socket import socket, SOCK_DGRAM, AF_INET
from functools import partial

#
# Add current and parent path to syspath
#
currentPath = os.path.dirname(__file__)
parentPath = os.path.abspath(os.path.join(currentPath, os.path.pardir))

paths = [
    currentPath,
    parentPath
]

for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

os.chdir(currentPath)


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


CATS = {'Actualités':
            {'path': '/Users/tarek/Dev/github.com/acr-dijon.org/content/actu'},
'Résultats':
            {'path': '/Users/tarek/Dev/github.com/acr-dijon.org/content/resultats'},

            }


def main():
    print('running app')

    #
    # Setup our pre-request plugin, session, debug mode, and methods
    # to serve static resources.
    #
    bottle.debug(DEBUG)

    # Uncomment line 84 and comment line 83 to enable session management
    app = bottle.app()
    app_stack.vars = app.vars = {'categories': CATS}
    app_stack.view = partial(view, **app.vars)

    from henet import views
    #app = SessionMiddleware(bottle.app(), config.SESSION_OPTS)
    run(app=app, host="localhost", port=BIND_TO_PORT)


if __name__ == '__main__':
    main()
