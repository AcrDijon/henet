# encoding: utf8
import datetime
from bottle import route, request, app, response, get
from henet.comments import ArticleThread, CommentsDB
from henet.events import emit, EVENT_CREATED_COMMENT


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


MODERATE_BODY = u"""\
Nouveau commentaire à modérer
"""


# XXX needs rate limiting
@route("/comments", method=['OPTIONS', 'POST'])
@enable_cors
def new_comment():
    data = request.json
    comments_dir = app._config['henet']['comments_dir']

    article_url = data['article_url']
    article_thread = ArticleThread(comments_dir, article_url)
    article_thread.add_comment(text=data['text'],
                               author=data['author'])

    article_thread.save()
    notifs = app._config['notifications']
    moderator = notifs.get('moderate_comment')
    if moderator is not None:
        app.send_email([moderator], u'Nouveau commentaire',
                       MODERATE_BODY)

    emit(EVENT_CREATED_COMMENT, article_url=article_url)
    return {'result': 'OK'}


@get("/comments")
@app.view("comments")
def get_comment():
    def add_summary(comment):
        if len(comment.text) > 20:
            comment.summary = comment.text[:20] + '...'
        else:
            comment.summary = comment.text
        return comment

    comments_dir = app._config['henet']['comments_dir']
    database = CommentsDB(comments_dir)
    comments = [add_summary(comment) for comment in
                database.get_moderation_queue()]

    return {'now': datetime.datetime.now(),
            'comments': comments, 'category': 'comments'}
