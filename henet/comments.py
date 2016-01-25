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
        self.articles = []

    def link_to_article(self, uuid):
        if uuid not in self.articles:
            self.articles.append(uuid)

    def save(self):
        if not self.thread:
            raise IOError("Not linked to a thread")
        # XXX unoptimal
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
            return date.strftime('%Y-%m-%d %H:%M')

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
        self.filename = os.path.join(self.storage_dir,
                                     'thread_' + self.uuid + '.rst')
        self.articles = []
        self.load()

    def link_to_article(self, uuid):
        if uuid not in self.articles:
            self.articles.append(uuid)

    @classmethod
    def loadfromfile(cls, filename):
        storage_dir = os.path.dirname(filename)
        basename = os.path.basename(filename)
        uuid = basename[len('thread_'):-len('.rst')]
        return Thread(storage_dir, uuid)

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
                          active=False, thread=self)
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
                      key=lambda comment: -comment.date.toordinal())

    def render(self):
        lines = [u':uuid: %s' % self.uuid, u'', u'----', u'']
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
        if self.thread is None:
            self.thread = Thread(self.storage_dir)
            self.save()
        return self.thread.add_comment(*args, **kw)

    def asjson(self):
        if self.thread is None:
            comments = []
        else:
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

        if self.thread is not None:
            self.thread.link_to_article(self.article_uuid)

    def render(self):
        return u'%s:%s' % (self.article_uuid, self.thread_uuid)

    @classmethod
    def loadfromfile(cls, filename):
        storage_dir = os.path.dirname(filename)
        cls = ArticleThread(storage_dir)
        cls.filename = filename
        cls.load()
        return cls


class CommentsDB(object):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

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

    def get_moderation_queue(self):
        comments = []

        for file in os.listdir(self.storage_dir):
            if not file.startswith('article_'):
                continue
            filename = os.path.join(self.storage_dir, file)
            article_thread = ArticleThread.loadfromfile(filename)
            thread = article_thread.thread
            for comment in thread.get_comments(include_inactive=True,
                                               include_active=False):
                if comment in comments:
                    continue
                comments.append(comment)
                yield comment
