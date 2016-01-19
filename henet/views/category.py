import os
from bottle import view, route, request, app
from henet.rst.parse import parse_article

from pelican.utils import slugify


# XXX todo indexing & caching
def by_date(article1, article2):
    return -cmp(article1['metadata']['date'], article2['metadata']['date'])


@route("/category/<name>")
@app.view("category")
def category(name):
    articles = []
    data = dict(app.vars['categories'])[name]
    path = data['path']

    for root, dirs, files in os.walk(path):
        for file_ in files:
            if not file_.endswith('.rst'):
                continue
            document = parse_article(os.path.join(root, file_))
            document['filename'] = os.path.join(root[len(path):], file_)
            articles.append(document)

    articles.sort(by_date)

    return {"category": name, 'articles': articles,
            "data": data}
