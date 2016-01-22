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
    emit(EVENT_CREATED_COMMENT, article_path=article_path)
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
