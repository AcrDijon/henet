import os
import datetime

from bottle import view, route, request, app, post, redirect
from pelican.utils import slugify
from henet.util import parse_articles


# XXX batch by year!
@route("/category/<name>")
@app.view("category")
def category(name):
    page = int(request.params.get('page', 0))
    data = dict(app.vars['categories'])[name]
    cache_dir = app._config['henet']['cache_dir']
    articles, total_pages = parse_articles(data['path'], cache_dir, page)

    return {"category": name, 'articles': articles,
            "data": data, "total_pages": total_pages,
            "current_page": page, "now": datetime.datetime.now()}



