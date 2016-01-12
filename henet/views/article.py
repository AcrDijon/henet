import os
from bottle import view, route, request, app
from henet.rst.parse import parse_article



@route("/category/<category>/<article>")
@app.view("article")
def article(category, article):
    cat_path = app.vars['categories'][category]['path']
    article_path = os.path.join(cat_path, article)
    document = parse_article(article_path)
    return {'article': document, 'category': category,
            'filename': article}
