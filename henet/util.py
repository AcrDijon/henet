import os
import hashlib
import bson
import datetime

from henet.rst.parse import parse_article as parse
from henet.article import Article


# XXX todo indexing & caching
def by_date(article1, article2):
    now = datetime.datetime.now()

    return -cmp(article1['metadata'].get('date', now).replace(tzinfo=None),
                article2['metadata'].get('date', now).replace(tzinfo=None))


def file_age(path):
    return os.stat(path).st_mtime


def md5(data):
    return hashlib.md5(data).hexdigest()


def parse_article(path, cache_dir, root_path):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    age = file_age(path)
    cache = os.path.join(cache_dir, md5(str(age)+path.encode('utf8')))
    if os.path.exists(cache):
        with open(cache) as f:
            article = Article(bson.loads(f.read()))
    else:
        article = parse(path)
        article['filename'] = path[len(root_path):]
        with open(cache, 'w') as f:
            f.write(bson.dumps(article))

    return article


def parse_articles(path, cache_dir, page=-1, page_size=20):
    articles = []
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if not file_.endswith('.rst'):
                continue
            fullpath = os.path.join(root, file_)
            articles.append(parse_article(fullpath, cache_dir, path))

    articles.sort(by_date)
    total_size = len(articles)
    total_pages, rest = divmod(total_size, page_size)
    if rest > 0:
        total_pages += 1

    if page != -1:
        start = page * page_size
        end = start + page_size - 1
        return articles[start:end], total_pages

    return articles, total_pages
