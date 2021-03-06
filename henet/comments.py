# encoding: utf8
"""
Comments Database.

A comment is described with the following fields:

- uuid: a unique id.
- author: the author of the comment
- text: the comment
- date: the date
- active: a flag indicating if the comment is active

I've made the design decision not to store the e-mail
or the website of the author in each comment to make
sure that a website that manages users will be able
to store user-related information separately and update
them without having to migrate all comments. The author
field can be used as a unique user identifier.

A thread is a collection of comments with its own uuid.
Last, an article has an uuid and can point to a thread.

The data is organized in a directory with two type of files:

- article_<huuid>.rst
- thread_<huuid>.rst

Where *huuid* is the md5 hash of the uuid.

The thread files contain its list of comment. It follows
the reStructuredText format and each comment is separated
with a transition marker.

The article file is a one-liner with just two fields:
the article uuid and the thread uuid.

Threads uuid can be auto-generated using uuid4() but articles
uuid should be a value uniquely identifying an article.

In Pelican, the path relative to the root content directory
is a good candidate because it allows Henet to store comments
related to an article no matter what the article URL is or
no matter what is the absolute path of the Pelican on disk.

Another important design decision is that a thread can be used
in several articles.
"""
import os
from uuid import uuid4
import datetime
import hashlib

from henet.rst.parse import parse_thread


class Comment(object):
    def __init__(self, uuid=None, text='', author='Anonymous',
                 date=None, active=True, thread=None):
        if uuid is None:
            uuid = str(uuid4())
        self.uuid = uuid
        self.text = text
        self.author = author
        if date is None:
            date = datetime.datetime.now()
        self.date = date
        self.thread = thread
        self.active = active
        # backrefs to articles
        self.articles = []

    def link_to_article(self, uuid):
        if uuid not in self.articles:
            self.articles.append(uuid)

    def save(self):
        if self.thread is None:
            return
        # XXX suboptimal
        self.thread.save()

    def asjson(self):
        res = {}
        res['uuid'] = self.uuid
        res['text'] = self.text
        res['author'] = self.author
        res['date'] = self.date
        res['active'] = self.active
        res['articles'] = self.articles
        return res

    def render(self):
        def _date2str(date):
            return date.strftime('%Y-%m-%d %H:%M:%S')

        def _bool2str(value):
            if value:
                return '1'
            return '0'

        lines = []
        for field, value in ((u'uuid', self.uuid),
                             (u'author', self.author),
                             (u'date', _date2str(self.date)),
                             (u'active', _bool2str(self.active))):
            lines.append(u':%s: %s' % (field, value))

        lines.append('')
        lines.append(self.text)
        return u'\n'.join(lines)


class Thread(object):

    def __init__(self, storage_dir, uuid=None):
        self.storage_dir = storage_dir
        if uuid is None:
            uuid = str(uuid4())
        self.uuid = uuid
        self.comments = []
        hashed_uuid = hashlib.md5(self.uuid).hexdigest()
        self.filename = os.path.join(self.storage_dir,
                                     'thread_' + hashed_uuid + '.rst')
        # backrefs to articles
        self.articles = []
        self.load()

    def link_to_article(self, uuid):
        if uuid not in self.articles:
            self.articles.append(uuid)
        for comment in self.comments:
            comment.link_to_article(uuid)

    @classmethod
    def loadfromfile(cls, filename):
        storage_dir = os.path.dirname(filename)
        klass = Thread(storage_dir)
        klass.filename = filename
        klass.load()
        return klass

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.render().encode('utf8'))

    def load(self):
        if not os.path.exists(self.filename):
            return
        self.uuid, comments = parse_thread(self.filename)
        self.comments = []
        for comment in comments:
            c = Comment(uuid=comment['uuid'], thread=self)
            c.author = comment.get('author', '')
            c.date = comment.get('date', datetime.datetime.now())
            c.text = comment.get('text', '').strip()
            c.active = comment.get('active', False)
            c.articles = self.articles
            self.comments.append(c)

    def add_comment(self, text, author='Anonymous', date=None,
                    active=False):
        comment = Comment(text=text, author=author, date=date,
                          active=active, thread=self)
        for article in self.articles:
            comment.link_to_article(article)
        self.comments.append(comment)
        return comment

    def activate_comment(self, cid):
        for comment in self.comments:
            if comment.uuid == cid:
                comment.active = True
                break

    def reject_comment(self, cid):
        self.comments = [comment for comment in self.comments
                         if comment.uuid != cid]

    def get_comment(self, uuid):
        for comment in self.comments:
            if comment.uuid == uuid:
                return comment
        raise KeyError(uuid)

    def get_comments(self, include_inactive=False, include_active=True):

        def selected(comment):
            return ((include_inactive and not comment.active) or
                    (include_active and comment.active))

        return sorted([comment for comment in self.comments
                       if selected(comment)],
                      key=lambda comment: comment.date, reverse=True)

    def render(self):
        lines = [u':uuid: %s' % self.uuid, u'']
        if len(self.comments) == 0:
            return u'\n'.join(lines)

        lines.extend([u'----', u''])
        for i, comment in enumerate(self.comments):
            lines.append(comment.render())
            if i == len(self.comments) - 1:
                break
            lines.append(u'')
            lines.append(u'----')
            lines.append(u'')

        return u'\n'.join(lines)


class ArticleThread(object):
    def __init__(self, storage_dir, article_uuid=None, thread_uuid=None):
        self.storage_dir = storage_dir
        if article_uuid is None:
            article_uuid = str(uuid4())
        self.article_uuid = article_uuid
        self.thread_uuid = thread_uuid
        self.thread = None
        hashed_uuid = hashlib.md5(self.article_uuid).hexdigest()
        self.filename = os.path.join(self.storage_dir,
                                     'article_' + hashed_uuid + '.rst')
        self.load()

    def add_comment(self, *args, **kw):
        return self.thread.add_comment(*args, **kw)

    def asjson(self):
        comments = [comment.asjson() for comment in
                    self.thread.get_comments()]

        return {'article_uuid': self.article_uuid,
                'thread_uuid': self.thread_uuid,
                'comments': comments}

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.render().encode('utf8'))
        self.thread.save()

    def load(self):
        if not os.path.exists(self.filename):
            self.thread = Thread(self.storage_dir, self.thread_uuid)
            self.thread_uuid = self.thread.uuid
        else:
            with open(self.filename) as f:
                uuids = f.read().split(':')
            self.article_uuid = uuids[0]
            self.thread_uuid = uuids[1]
            self.thread = Thread(self.storage_dir, self.thread_uuid)

        self.thread.link_to_article(self.article_uuid)

    def render(self):
        return u'%s:%s' % (self.article_uuid, self.thread_uuid)

    @classmethod
    def loadfromfile(cls, filename):
        storage_dir = os.path.dirname(filename)
        klass = ArticleThread(storage_dir)
        klass.filename = filename
        klass.load()
        return klass


class CommentsDB(object):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def _get_comment(self, uuid):
        thread = comment = None
        for file in os.listdir(self.storage_dir):
            if not file.startswith('thread_'):
                continue
            filename = os.path.join(self.storage_dir, file)
            thread = Thread.loadfromfile(filename)
            try:
                comment = thread.get_comment(uuid)
                break
            except KeyError:
                pass
        if comment is None:
            thread = None
        return thread, comment

    def activate_comment(self, uuid):
        thread, comment = self._get_comment(uuid)
        if thread is not None:
            thread.activate_comment(comment.uuid)
            thread.save()

    def reject_comment(self, uuid):
        thread, comment = self._get_comment(uuid)
        if thread is not None:
            thread.reject_comment(comment.uuid)
            thread.save()

    def _get_comments(self, inactive=True, active=False,
                      article_uuid=None):
        for file in os.listdir(self.storage_dir):
            if not file.startswith('article_'):
                continue
            filename = os.path.join(self.storage_dir, file)
            article_thread = ArticleThread.loadfromfile(filename)
            thread = article_thread.thread

            if (article_uuid is not None and
                    article_thread.article_uuid != article_uuid):
                continue

            for comment in thread.get_comments(include_inactive=inactive,
                                               include_active=active):
                yield comment

    def get_moderation_queue(self):
        return self._get_comments()

    def get_comments(self, article_uuid=None):
        return self._get_comments(inactive=False, active=True,
                                  article_uuid=article_uuid)
