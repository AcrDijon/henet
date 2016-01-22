# -*- coding: utf-8 -*-
from pelican import signals
from henet.comments import ArticleThread
from henet.rst.rst2html import rst2html


storage_dir = '/tmp/comments'


# xxx cache
def add_comments(generator, content):
    thread = ArticleThread(storage_dir, content.url)
    thread = thread.asjson()
    for comment in thread['comments']:
        comment['text'] = rst2html(comment['text'], theme='acr')
    content.metadata["comments"] = thread


def register():
    signals.article_generator_write_article.connect(add_comments)
