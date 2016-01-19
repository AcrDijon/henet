import os
import hashlib

import bson
from henet.rst.parse import parse_article


# XXX todo indexing & caching
def by_date(article1, article2):
    return -cmp(article1['metadata']['date'].replace(tzinfo=None),
                article2['metadata']['date'].replace(tzinfo=None))


def file_age(path):
    return os.stat(path).st_mtime


def md5(data):
    return hashlib.md5(data).hexdigest()


def parse_articles(path, cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    articles = []
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if not file_.endswith('.rst'):
                continue
            fullpath = os.path.join(root, file_)
            age = file_age(fullpath)
            filename = os.path.join(root[len(path):], file_)
            filename = filename.encode('utf8')
            cache = os.path.join(cache_dir, md5(str(age)+filename))

            if os.path.exists(cache):
                with open(cache) as f:
                    document = bson.loads(f.read())
            else:
                document = parse_article(os.path.join(root, file_))
                document['filename'] = filename
                with open(cache, 'w') as f:
                    f.write(bson.dumps(document))

            articles.append(document)

    articles.sort(by_date)
    return articles
