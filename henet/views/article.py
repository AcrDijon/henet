# coding: utf8
import os
import datetime

from bottle import route, request, app, post, redirect
from pelican.utils import slugify
from bottle_utils.csrf import csrf_protect, csrf_token
from bottle_utils.i18n import lazy_gettext as _

from henet.util import parse_article
from henet.article import Article
from henet.events import (emit, EVENT_CHANGED_CONTENT, EVENT_CREATED_CONTENT,
                          EVENT_DELETED_CONTENT)


@post("/delete/category/<category>/<article:path>", no_i18n=True)
@csrf_protect
def del_article(category, article):
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    os.remove(article_path)
    emit(EVENT_DELETED_CONTENT, article_path=article_path)
    redirect('/category/%s' % category)


@post("/delete/page/<page>/<article:path>", no_i18n=True)
@csrf_protect
def del_page(page, article):
    page_path = dict(app.vars['pages'])[page]['path']
    article_path = os.path.join(page_path, article)
    os.remove(article_path)
    emit(EVENT_DELETED_CONTENT, article_path=article_path)
    redirect('/page/%s' % page)


@route("/page/<page>/<article:path>")
@app.view("page")
@csrf_token
def get_page(page, article):
    cache_dir = app._config['henet']['cache_dir']
    page_path = dict(app.vars['pages'])[page]['path']
    article_path = os.path.join(page_path, article)
    article = parse_article(article_path, cache_dir, page_path)
    return {'article': article, 'page': page,
            'now': datetime.datetime.now(),
            'csrf_token': request.csrf_token,
            'filename': os.path.split(article_path)[-1]}


@route("/category/<category>/<article:path>")
@app.view("article")
@csrf_token
def get_article(category, article):
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    article = parse_article(article_path, cache_dir, cat_path)
    return {'article': article, 'category': category,
            'now': datetime.datetime.now(),
            'csrf_token': request.csrf_token,
            'filename': os.path.split(article_path)[-1]}


@post("/page/<page>/<article:path>", no_i18n=True)
@csrf_protect
def post_page(page, article):
    data = dict(request.POST.decode())
    cache_dir = app._config['henet']['cache_dir']
    page_path = dict(app.vars['pages'])[page]['path']
    article_path = os.path.join(page_path, article)
    article = parse_article(article_path, cache_dir, page_path)

    # XXX all this update crap should be in a Document() class
    if 'title' in data:
        article['title'] = data['title']
    if 'body' in data:
        article['body'] = data['body']
    if 'date' in data:
        article.set_metadata('date', data['date'])

    with open(article_path, 'w') as f:
        f.write(article.render().encode('utf8'))

    emit(EVENT_CHANGED_CONTENT, article_path=article_path)
    redirect('/page/%s/%s' % (page, article['filename']))


@post("/category/<category>/<article:path>", no_i18n=True)
@csrf_protect
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

    emit(EVENT_CHANGED_CONTENT, article_path=article_path)
    redirect('/category/%s/%s' % (category, article['filename']))


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


@post("/create", no_i18n=True)
@csrf_protect
def create_article_or_page():
    data = dict(request.POST.decode())
    category = u'resultats'
    page = None

    for key, val in data.items():
        if key.startswith(u'cat_add_'):
            category = key[len(u'cat_add_'):]
            break
        if key.startswith(u'page_add_'):
            page = key[len(u'page_add_'):]
            break

    title = data.get('title', u'').strip()
    if len(title) == 0:
        # nope
        app.add_alert(_('A title is required.'))
        if page is None:
            redirect('/category/%s' % category)
        else:
            redirect('/page/%s' % page)
        return

    article = Article()
    article['title'] = data['title']
    article['body'] = data.get('body', DEFAULT_BODY)
    date = datetime.datetime.now()
    article.set_metadata('date', date)

    if page is None:
        # it's an article
        article.set_metadata('category', category)
        path = dict(app.vars['categories'])[category]['path']
    else:
        # it's a page
        path = dict(app.vars['pages'])[page]['path']

    # XXX we might want to put it under the year directory
    i = 1
    filename = slugify(article['title'])
    fullfilename = os.path.join(path, filename)
    while os.path.exists(fullfilename + '.rst'):
        fullfilename += str(i)
        i += 1

    with open(fullfilename + '.rst', 'w') as f:
        f.write(article.render().encode('utf8'))

    emit(EVENT_CREATED_CONTENT, article_path=fullfilename)
    if page is None:
        redirect('/category/%s/%s' % (category, filename + '.rst'))
    else:
        redirect('/page/%s/%s' % (page, filename + '.rst'))
