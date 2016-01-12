import os
from bottle import view, route, request, app
from henet.rst.rst2html import rst2html



@route("/category/<category>/<article>/preview")
def article(category, article):
    cat_path = app.vars['categories'][category]['path']
    article_path = os.path.join(cat_path, article)
    with open(article_path) as f:
        return rst2html(f.read(), theme='acr')
