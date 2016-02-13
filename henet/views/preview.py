from bottle import request, post, get
from bottle_utils.i18n import lazy_gettext as _
from henet.rst.rst2html import rst2html
from henet.util import md5


@get("/preview")
def get_preview():
    return _('Loading...')


# XXX make this redis
_CACHE = {}


@post("/preview", no_i18n=True)
def build_preview():
    rst = request.json.get('rst', '')
    key = md5(rst)
    if key in _CACHE:
        return _CACHE[key]
    res = rst2html(rst, theme='acr')
    _CACHE[key] = res
    return res
