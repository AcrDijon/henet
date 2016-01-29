from bottle import route, app
from henet.util import content_changed


@route("/")
@app.view("home")
def home():
    cache_dir = app._config['henet']['cache_dir']
    content_dir = app._config['henet']['pelican_content_path']
    changed = content_changed(content_dir, cache_dir)
    return {'content_changed': changed}
