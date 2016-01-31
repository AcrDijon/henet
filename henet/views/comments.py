# encoding: utf8
import datetime
from bottle import route, request, app, response, get, post, redirect
from bottle_utils.csrf import csrf_protect, csrf_token

from henet.comments import ArticleThread, CommentsDB
from henet.events import emit, EVENT_CREATED_COMMENT
from henet.rst.rst2html import rst2html


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
    article_uuid = data['source_path']
    article_thread = ArticleThread(comments_dir, article_uuid)
    article_thread.add_comment(text=data['text'],
                               author=data['author'])

    article_thread.save()
    notifs = app._config['notifications']
    moderator = notifs.get('moderate_comment')
    if moderator is not None:
        app.send_email([moderator], u'Nouveau commentaire',
                       MODERATE_BODY)

    emit(EVENT_CREATED_COMMENT, article_uuid=article_uuid)
    return {'result': 'OK'}


@post("/comments/<comment_id>/activate")
@csrf_protect
def activate_comment(comment_id):
    comments_dir = app._config['henet']['comments_dir']
    database = CommentsDB(comments_dir)
    database.activate_comment(comment_id)
    redirect('/comments')


@post("/comments/<comment_id>/reject")
@csrf_protect
def reject_comment(comment_id):
    comments_dir = app._config['henet']['comments_dir']
    database = CommentsDB(comments_dir)
    database.reject_comment(comment_id)
    redirect('/comments')


@get("/comments")
@app.view("comments")
@csrf_token
def get_comment():
    def add_summary(comment):
        if len(comment.text) > 20:
            comment.summary = comment.text[:20] + '...'
        else:
            comment.summary = comment.text

        comment.html = rst2html(comment.text, theme='acr', body_only=True)
        return comment

    comments_dir = app._config['henet']['comments_dir']
    database = CommentsDB(comments_dir)
    comments = [add_summary(comment) for comment in
                database.get_moderation_queue()]

    return {'now': datetime.datetime.now(),
            "csrf_token": request.csrf_token,
            'comments': comments, 'category': 'comments'}
