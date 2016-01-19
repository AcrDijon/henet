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
    path = dict(app.vars['categories'])[name]['path']
    for file_ in os.listdir(path):
        if not file_.endswith('.rst'):
            continue

        document = parse_article(os.path.join(path, file_))
        document['filename'] = file_
        url = '/posts/%s/%s/%s/%s'
        url = url % ('2016', '01', '11', slugify(document['title']))
        document['url'] = url

        articles.append(document)

    articles.sort(by_date)
    return {"category": name, 'articles': articles}
