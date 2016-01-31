import datetime
from bottle import route, request, app
from bottle_utils.csrf import csrf_token
from pelican.utils import slugify
from henet.util import parse_articles


@route("/page/<name>")
@app.view("pages")
@csrf_token
def page(name):
    page = int(request.params.get('page', 0))
    data = dict(app.vars['pages'])[name]
    cache_dir = app._config['henet']['cache_dir']
    site_url = app._config['henet']['site_url']
    page_url = app._config['henet']['pages_url']
    page_url = site_url + '/' + page_url
    page_path = data['path']

    def set_extra_info(article):
        data = {'date': article['metadata']['date'],
                'slug': slugify(article['title'])}
        article['url'] = page_url.format(**data)
        return article

    articles, total_pages = parse_articles(page_path, cache_dir, page)
    articles = [set_extra_info(article) for article in articles]

    return {"page": name, 'articles': articles,
            "data": data, "total_pages": total_pages,
            "can_create": data['can_create'],
            "csrf_token": request.csrf_token,
            "current_page": page, "now": datetime.datetime.now()}
