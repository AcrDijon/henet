import os
from bottle import view, route, request, app, post, get

from henet.rst.rst2html import rst2html
from henet.rst.parse import parse_article

@get("/preview")
def get_preview():
    return 'Loading...'


@post("/preview")
def build_preview():
    rst = request.POST['rst']
    return rst2html(rst, theme='acr')
