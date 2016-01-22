from bottle import route, request, app, response
from henet.comments import ArticleThread


def enable_cors(func):
    def _enable_cors(*args, **kwargs):
        hds = response.headers
        hds['Access-Control-Allow-Origin'] = '*'
        hds['Access-Control-Allow-Methods'] = ', '.join(['PUT', 'GET',
                                                         'POST', 'DELETE',
                                                         'OPTIONS'])
        allow = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        hds['Access-Control-Allow-Headers'] = allow
        if request.method != 'OPTIONS':
            return func(*args, **kwargs)
    return _enable_cors


@route("/comments", method=['OPTIONS', 'POST'])
@enable_cors
def new_comment():
    data = request.json
    comments_dir = app._config['henet']['comments_dir']

    article_thread = ArticleThread(comments_dir, data['article_url'])
    article_thread.add_comment(text=data['text'],
                               author=data['author'])

    # XXX trigger mail for moderation
    article_thread.save()
    return {'result': 'OK'}
