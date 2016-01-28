import subprocess
from bottle import post, app, redirect
from henet.events import emit, EVENT_BUILD, EVENT_ALREADY_BUILDING


def _run(command):
    return subprocess.call(command, shell=True)


@post("/build")
def build():
    if app.workers.in_progress('build-pelican'):
        emit(EVENT_ALREADY_BUILDING)
        redirect('/')
        return

    cmd = app._config['henet']['build_command']
    app.workers.apply_async('build-pelican', _run, (cmd,))
    emit(EVENT_BUILD)
    redirect('/')
