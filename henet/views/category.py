import os
from bottle import view, route, request, app
from pelican.utils import slugify

from henet.util import parse_articles

@route("/category/<name>")
@app.view("category")
def category(name):
    data = dict(app.vars['categories'])[name]
    cache_dir = app._config['henet']['cache_dir']
    articles = parse_articles(data['path'], cache_dir)

    return {"category": name, 'articles': articles,
            "data": data}
