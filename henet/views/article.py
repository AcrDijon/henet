# coding: utf8
import os
import datetime

from bottle import route, request, app, post, redirect
from pelican.utils import slugify

from henet.util import parse_article
from henet.article import Article


@route("/category/<category>/<article:path>")
@app.view("article")
def get_article(category, article):
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    article = parse_article(article_path, cache_dir, cat_path)
    return {'article': article, 'category': category,
            'now': datetime.datetime.now(),
            'filename': os.path.split(article_path)[-1]}


@post("/category/<category>/<article:path>")
def post_article(category, article):
    data = dict(request.POST.decode())
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    article = parse_article(article_path, cache_dir, cat_path)

    # XXX all this update crap should be in a Document() class
    if 'title' in data:
        article['title'] = data['title']
    if 'body' in data:
        article['body'] = data['body']

    for meta in ('location', 'date', 'eventdate'):
        if meta in data:
            article.set_metadata(meta, data[meta])

    with open(article_path, 'w') as f:
        f.write(article.render().encode('utf8'))

    redirect('/category/%s%s' % (category, article['filename']))


DEFAULT_BODY = u"""
Voici un exemple de texte.

**Texte en gras**

*Texte en italique*

Voici une liste:

- un
- deux
- trois

Attention à bien sauter une ligne avant ET apres la liste!

Une image:

.. image:: http://assets.acr-dijon.org/1janvacr1.jpg

"""


@post("/create")
def create_article():
    data = dict(request.POST.decode())
    article = Article()

    article['title'] = data['title']
    article['body'] = data.get('body', DEFAULT_BODY)

    date = datetime.datetime.now()
    article.set_metadata('date', date)

    if u'add_actus' in data:
        category = u'actus'
    elif u'add_foulees' in data:
        category = u'foulees'
    else:
        category = u'resultats'

    article.set_metadata('category', category)

    cat_path = dict(app.vars['categories'])[category]['path']
    # XXX we might want to put it under the year directory
    i = 1
    filename = slugify(article['title'])
    fullfilename = os.path.join(cat_path, filename)
    while os.path.exists(fullfilename + '.rst'):
        fullfilename += str(i)
        i += 1

    with open(fullfilename + '.rst', 'w') as f:
        f.write(article.render().encode('utf8'))

    redirect('/category/%s/%s' % (category, filename + '.rst'))
