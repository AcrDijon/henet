# coding: utf8
import os
import datetime

from bottle import view, route, request, app, post, redirect
from henet.util import parse_article
from pelican.utils import slugify


@route("/category/<category>/<article:path>")
@app.view("article")
def article(category, article):
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    document = parse_article(article_path, cache_dir, cat_path)
    return {'article': document, 'category': category,
            'filename': os.path.split(article)[-1]}


@post("/category/<category>/<article:path>")
def article(category, article):
    data = dict(request.POST.decode())
    cache_dir = app._config['henet']['cache_dir']
    cat_path = dict(app.vars['categories'])[category]['path']
    article_path = os.path.join(cat_path, article)
    document = parse_article(article_path, cache_dir, cat_path)

    # XXX all this update crap should be in a Document() class
    if 'title' in data:
        title = data['title']
        document['title'] = title
        document['title_source'] = title + u'\n' + u'=' * len(title)
    if 'body' in data:
        document['body'] = data['body']

    for meta in ('location', 'date', 'eventdate'):
        if meta in data:
            document['metadata'][meta] = data[meta]
    metadata = [u':%s: %s' % (name, value) for name, value in
                document['metadata'].items()]
    metadata = u'\n'.join(metadata)
    document['metadata_source'] = metadata

    render = [document['title_source'], u'',
              document['metadata_source'], u'',
              document['body'], u'']

    with open(article_path, 'w') as f:
        f.write(u'\n'.join(render).encode('utf8'))

    redirect('/category/%s%s' % (category, document['filename']))


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
    title = data['title']
    body = data.get('body', DEFAULT_BODY)
    date = datetime.datetime.now()
    if u'add_actus' in data:
        category = u'actus'
    elif u'add_foulees' in data:
        category = u'foulees'
    else:
        category = u'resultats'

    metadata = {'date': unicode(date.strftime('%Y-%m-%d %H:%M')),
                'category': category}

    cat_path = dict(app.vars['categories'])[category]['path']
    # XXX we might want to put it under the year directory
    i = 1
    filename = slugify(title)
    fullfilename = os.path.join(cat_path, filename)
    while os.path.exists(fullfilename + '.rst'):
        fullfilename += str(i)
        i += 1

    metadata = [u':%s: %s' % (name, value) for name, value in metadata.items()]
    metadata = u'\n'.join(metadata)
    document = [title, u'=' * len(title), u'', metadata, u'', body, u'']

    with open(fullfilename + '.rst', 'w') as f:
        f.write(u'\n'.join(document).encode('utf8'))

    redirect('/category/%s/%s' % (category, filename + '.rst'))
