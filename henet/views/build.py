import os
import subprocess
from functools import partial

from bottle import post, app, redirect, request
from bottle_utils.csrf import csrf_protect

from henet.events import (emit, EVENT_BUILT, EVENT_ALREADY_BUILDING,
                          EVENT_START_BUILDING)
from henet.util import save_build_hash


def _run(command, wdir):
    return subprocess.call([command], cwd=wdir, shell=True)


@post("/build", no_i18n=True)
@csrf_protect
def build():

    if app.workers.in_progress('build-pelican'):
        emit(EVENT_ALREADY_BUILDING)
        redirect('/')
        return

    cache_dir = app._config['henet']['cache_dir']
    content_dir = app._config['henet']['pelican_content_path']
    cmd = app._config['henet']['build_command']
    cmd_dir = app._config['henet'].get('build_working_dir', os.getcwd())

    client_id = request.remote_addr

    def done_building(client_id, *args):
        save_build_hash(content_dir, cache_dir)
        emit(EVENT_BUILT, client_id=client_id)

    done_building = partial(done_building, client_id)

    app.workers.apply_async('build-pelican', _run, (cmd, cmd_dir),
                            done_building)
    emit(EVENT_START_BUILDING)
    redirect('/')
