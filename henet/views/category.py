import os
import datetime
from bottle import route, request, app
from pelican.utils import slugify

from henet.util import parse_articles
from henet.comments import CommentsDB


# XXX batch by year!
@route("/category/<name>")
@app.view("category")
def category(name):
    page = int(request.params.get('page', 0))
    data = dict(app.vars['categories'])[name]
    cache_dir = app._config['henet']['cache_dir']
    site_url = app._config['henet']['site_url']
    article_url = app._config['henet']['article_url']
    article_url = site_url + '/' + article_url
    content_root = app._config['henet']['pelican_content_path']
    comments_dir = app._config['henet']['comments_dir']
    comments_database = CommentsDB(comments_dir)
    cat_path = data['path']

    def set_extra_info(article):
        data = {'date': article['metadata']['date'],
                'slug': slugify(article['title'])}
        article['url'] = article_url.format(**data)
        article_filename = os.path.join(cat_path, article['filename'])
        article_uuid = article_filename[len(content_root) + 1:]
        comments = comments_database.get_comments(article_uuid=article_uuid)
        article['comments_count'] = len(list(comments))
        return article

    articles, total_pages = parse_articles(cat_path, cache_dir, page)
    articles = [set_extra_info(article) for article in articles]

    return {"category": name, 'articles': articles,
            "data": data, "total_pages": total_pages,
            "can_create": data['can_create'],
            "current_page": page, "now": datetime.datetime.now()}
