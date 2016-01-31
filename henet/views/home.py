from bottle import route, app, request
from henet.util import content_changed
from bottle_utils.csrf import csrf_token


@route("/")
@app.view("home")
@csrf_token
def home():
    cache_dir = app._config['henet']['cache_dir']
    content_dir = app._config['henet']['pelican_content_path']
    changed = content_changed(content_dir, cache_dir)
    return {'content_changed': changed, "csrf_token": request.csrf_token}
