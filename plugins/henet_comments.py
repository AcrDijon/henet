# -*- coding: utf-8 -*-
from pelican import signals
from henet.comments import ArticleThread
from henet.rst.rst2html import rst2html


# xxx read config
storage_dir = '/Users/tarek/Dev/github.com/acr-dijon.org/comments/'


# xxx cache
def add_comments(generator, content):
    thread = ArticleThread(storage_dir, content.url)
    thread = thread.asjson()
    for comment in thread['comments']:
        # XXX rst2html renders a whole html page, we just want an
        # html snippet we can add in our page
        comment['text'] = rst2html(comment['text'], theme='acr')
    content.metadata["comments"] = thread


def register():
    signals.article_generator_write_article.connect(add_comments)
