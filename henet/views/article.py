import os
from bottle import view, route, request, app
from henet.util import parse_article


@route("/category/<category>/<article:path>")
@app.view("article")
def article(category, article):
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    document = parse_article(article_path, cache_dir, cat_path)
    return {'article': document, 'category': category,
            'filename': os.path.split(article)[-1]}
