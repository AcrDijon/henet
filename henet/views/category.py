import os
from bottle import view, route, request, app
from henet.rst.parse import parse_article


@route("/category/<name>")
@app.view("category")
def category(name):
    articles = []
    path = app.vars['categories'][name]['path']
    for file_ in os.listdir(path):
        if not file_.endswith('.rst'):
            continue

        document = parse_article(os.path.join(path, file_))
        document['filename'] = file_
        articles.append(document)

    return {"category": name, 'articles': articles}
