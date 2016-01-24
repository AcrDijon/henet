# encoding: utf-8
import signal
import sys
import os
from functools import partial
from logging.config import fileConfig

import bottle
from bottle import route, run, view, app as app_stack
from bottle import static_file
import konfig

from henet.events import subscribe, ALL_EVENTS, event2str
from henet.pool import initialize_pool, close_pool, apply_async
from henet.util import send_email
from henet import logger
import multiprocessing_logging


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


_alerts = []


def add_alert(event, **data):
    # per-thread ? per-user ?
    _alerts.append(event2str(event))


def get_alerts():
    while True:
        try:
            yield _alerts.pop()
        except IndexError:
            break


def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = DEFAULT_CONFIG

    fileConfig(config_file)
    multiprocessing_logging.install_mp_handler()

    config = konfig.Config(config_file)
    bottle.debug(config['henet'].get('debug', DEFAULT_DEBUG))

    app = bottle.app()
    cats = []
    for cat in config['henet']['categories']:
        values = dict(config[cat].items())
        # defaults
        if 'can_create' not in values:
            values['can_create'] = True
        cats.append((cat, values))

    app_stack.vars = app.vars = {'categories': cats, 'get_alerts': get_alerts}
    app_stack.view = partial(view, **app.vars)
    app_stack._config = app._config = config
    smtp_config = dict(config.items('smtp'))

    def _send_email(*args):
        args = list(args) + [smtp_config]
        apply_async(send_email, args)

    app_stack.send_email = app.send_email = _send_email

    from henet import views  # NOQA

    def _close_pool(*args):
        close_pool()
        sys.exit(0)

    subscribe(ALL_EVENTS, add_alert)
    signal.signal(signal.SIGINT, _close_pool)
    initialize_pool()
    run(app=app,
        host=config['henet'].get('host', DEFAULT_HOST),
        port=config['henet'].get('port', DEFAULT_PORT),
        server='waitress')


if __name__ == '__main__':
    main()
