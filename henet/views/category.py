import datetime
from bottle import route, request, app
from henet.util import parse_articles
from pelican.utils import slugify


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

    def set_url(article):
        data = {'date': article['metadata']['date'],
                'slug': slugify(article['title'])}
        article['url'] = article_url.format(**data)
        return article

    articles, total_pages = parse_articles(data['path'], cache_dir, page)
    articles = [set_url(article) for article in articles]

    return {"category": name, 'articles': articles,
            "data": data, "total_pages": total_pages,
            "current_page": page, "now": datetime.datetime.now()}
