# -*- coding: utf-8 -*-
import traceback

from pelican import signals

from henet.comments import ArticleThread
from henet.rst.rst2html import rst2html


# xxx read config
storage_dir = '/Users/tarek/Dev/github.com/acr-dijon.org/comments/'


# xxx cache
def add_comments(generator, content):
    try:
        # the article unique id is its relative source path,
        # so the comments are not dependant on the URL.
        source_path = content.get_relative_source_path()
        article_uuid = source_path.encode('utf8')
        thread = ArticleThread(storage_dir, article_uuid)
        thread = thread.asjson()

        for comment in thread['comments']:
            html = rst2html(comment['text'], theme='acr', body_only=True)
            comment['html'] = html

        content.metadata["comments"] = thread
    except:
        # XXX for some reason Pelican does not print plugins exceptions
        traceback.print_exc()
        raise

def register():
    signals.article_generator_write_article.connect(add_comments)
