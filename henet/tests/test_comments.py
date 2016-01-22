# encoding: utf8
import unittest
import tempfile
import shutil
import datetime

from henet.comments import Thread, ArticleThread, CommentsDB


class TestThread(unittest.TestCase):

    def setUp(self):
        self.tempdirs = []

    def tearDown(self):
        for tempdir in self.tempdirs:
            shutil.rmtree(tempdir)

    def get_tempdir(self):
        tempdir = tempfile.mkdtemp()
        self.tempdirs.append(tempdir)
        return tempdir

    def test_storage(self):
        tempdir = self.get_tempdir()
        thread = Thread(tempdir)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=1)
        way_later = later + datetime.timedelta(days=15)

        c1 = thread.add_comment(u"Ouai **ouai1**", date=now)
        thread.add_comment(u"Ouai **ouai**", date=later)
        c3 = thread.add_comment(u"Ouai **ouai3**", date=way_later)

        thread.activate_comment(c1.uuid)
        thread.activate_comment(c3.uuid)

        thread.save()
        thread.load()

        # we have 2 active comments
        comments = thread.get_comments()
        self.assertEqual(len(comments), 2)

        comments = thread.get_comments(include_inactive=True)
        self.assertEqual(len(comments), 3)
        comment = comments[0]

        # most recent first
        self.assertEqual(comment.text, u"Ouai **ouai3**")

    def test_article_thread(self):
        tempdir = self.get_tempdir()
        thread = Thread(tempdir)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=1)
        way_later = later + datetime.timedelta(days=15)

        c1 = thread.add_comment(u"Ouai **ouai**", date=now)
        thread.add_comment(u"Ouai **ouai**", date=later)
        c3 = thread.add_comment(u"Ouai **ouai3**", date=way_later)

        thread.activate_comment(c1.uuid)
        thread.activate_comment(c3.uuid)
        thread.save()

        article_thread = ArticleThread(tempdir, '/post/mypost',
                                       thread.uuid)

        article_thread.save()
        article_thread.load()

        thread = article_thread.thread

        # we have 2 active comments
        comments = thread.get_comments()
        self.assertEqual(len(comments), 2)

        comments = thread.get_comments(include_inactive=True)
        self.assertEqual(len(comments), 3)
        comment = comments[0]

        # most recent first
        self.assertEqual(comment.text, u"Ouai **ouai3**")

        # let's check the moderation queue
        comments = CommentsDB(tempdir)

        for comment in comments.get_moderation_queue():
            comment.active = True
            comment.save()    # should automate this

        # we have 3 active comments now
        thread.load()
        comments = thread.get_comments()
        self.assertEqual(len(comments), 3)