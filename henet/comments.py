import os
from uuid import uuid4
import datetime

from henet.rst.parse import parse_thread


class Comment(object):
    def __init__(self, uuid=None, title='', text='', author='Anonymous',
                 date=None):
        if uuid is None:
            uuid = str(uuid4())
        self.uuid = uuid
        self.title = title
        self.text = text
        self.author = author
        if date is None:
            date = datetime.datetime.now()
        self.date = date

    def render(self):
        def _date2str(date):
            return date.strftime('%Y-%m-%d %H:%M')

        lines = []
        for field, value in ((u'uuid', self.uuid),
                             (u'title', self.title),
                             (u'author', self.author),
                             (u'date', _date2str(self.date))):

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
        self.filename = os.path.join(self.storage_dir, self.uuid + '.rst')
        self.load()

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.render().encode('utf8'))

    def load(self):
        if not os.path.exists(self.filename):
            return
        self.uuid, comments = parse_thread(self.filename)
        self.comments = []
        for comment in comments:
            c = Comment(uuid=comment['uuid'])
            c.title = comment.get('title', '')
            c.author = comment.get('author', '')
            c.date = comment.get('date', datetime.datetime.now())
            c.text = comment.get('text', '').strip()
            self.comments.append(c)

    def add_comment(self, title, text, author='Anonymous', date=None):
        comment = Comment(title=title, text=text, author=author, date=date)
        self.comments.append(comment)
        return comment

    def modify_comment(self, cid, **fields):
        pass

    def delete_comment(self, cid):
        pass

    def get_comments(self):
        return sorted(self.comments, key=lambda comment:
                      -comment.date.toordinal())

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
