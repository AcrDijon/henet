import os
from bottle import view, route, request, app, post

from henet.rst.rst2html import rst2html
from henet.rst.parse import parse_article



@route("/category/<category>/<article>/preview")
def article(category, article):
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    document = parse_article(article_path)
    return rst2html(document['body'], theme='acr')


@post("/preview")
def build_preview():
    rst = request.POST['rst']
    return rst2html(rst, theme='acr')
